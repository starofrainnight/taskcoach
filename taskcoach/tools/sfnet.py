#!/usr/bin/env python

## Task Coach - Your friendly task manager
## Copyright (C) 2009 Jerome Laheurte <fraca7@free.fr>

## Task Coach is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## Task Coach is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

SF.net automation.

When using IE8,

 * Enable 'Display mixed content' in the Misc section of the security
   settings for the Internet zone.
 * Disable flash! It makes IE crash on sourceforge!

"""

import PAM


def allChildren(elt):
    """Returns all children of a IHTMLElement, recursively"""

    children = []

    for child in elt.children:
        children.append(child)
        children.extend(allChildren(child))

    return children


class SourceForge(PAM.PAMIE):
    def __init__(self, projectName):
        PAM.PAMIE.__init__(self, 'https://sourceforge.net/account/login.php')

        self.__projectName = projectName

    def login(self, user, pwd):
        if not (self.setTextBox('form_loginname', user) and \
                self.setTextBox('form_pw', pwd) and \
                self.clickButton('login')):
            raise RuntimeError('Could not login')

    def logout(self):
        self.clickLink('Log out')

    def addRelease(self, releaseName):
        """This assumes default package"""

        if not self.navigate('https://sourceforge.net/projects/%s/develop' % self.__projectName):
            raise RuntimeError('Could not go to project page')

        elt = self.findElement('li', 'id', 'menu_frs')
        if elt is None:
            raise RuntimeError('Could not find FRS link')

        # Trying to click it raises a COM error.
        self.navigate(elt.children[0].getAttribute('href'))

        link = self.findElement('a', 'href', r'!.*/newrelease\.php')
        if link is None:
            raise RuntimeError('Could not find add release link')
        self.clickElement(link)

        if not self.setTextBox('release_name', releaseName):
            raise RuntimeError('Unable to set release name.')

        if not self.clickButton('Create This Release'):
            raise RuntimeError('Cannot find create release button')

    def editRelease1(self, notes, changes, files):
        """Release notes, changelog, uploaded files."""

        if not (self.setTextArea('release_notes', notes) and \
                self.setTextArea('release_changes', changes)):
            raise RuntimeError('Cannot set release notes/changes')

        self.clickButton('Submit/Refresh')

        for button in self.getElementsList('input', 'type=checkbox;name=file_list[]'):
            if button.getAttribute('value') in files:
                files.remove(button.getAttribute('value'))
                button.click()

        if files:
            print 'WARNING: the following files were not found:'
            print '\n'.join(files)

            r = raw_input('Continue anyway [y/N] ? ').strip()
            if r.lower() != 'y':
                raise RuntimeError('Error adding files to release.')

        self.clickButton('Add Files and/or Refresh View')

    def editRelease2(self, files):
        """Arch/file type. 'files' is a list of 3-tuples (file name,
        arch, type)."""

        for filename, arch, fileType in files:
            self._wait()

            # Okay, this is particularly ugly. A better way to do this
            # would be to loop over 'form' elements, but since these
            # ones are *outside* the <tr></tr> block, they don't
            # appear in the DOM! WTF ? Anyway...

            elt = self.findElement('font', 'innerHTML', filename)
            if elt is None:
                print 'WARNING! could not find form for file %s' % filename
                continue

            trElt = elt.parentElement.parentElement

            for child in allChildren(trElt):
                if child.tagName.lower() == 'select' and child.getAttribute('name') == 'processor_id':
                    for choice in child.children:
                        if choice.innerText == arch:
                            choice.selected = True
                            break
                    else:
                        raise RuntimeError('Could not find arch %s for file %s' % (arch, filename))

            for child in allChildren(trElt):
                if child.tagName.lower() == 'select' and child.getAttribute('name') == 'type_id':
                    for choice in child.children:
                        if choice.innerText == fileType:
                            choice.selected = True
                            break
                    else:
                        raise RuntimeError('Could not find type %s for file %s' % (fileType, filename))

            # And of course, the submit button is in the *next* <tr>... Sigh...

            state = 0
            for input in allChildren(trElt.parentElement):
                if state == 0:
                    if input == trElt:
                        state = 1
                elif state == 1:
                    if input.tagName.lower() == 'input' and input.getAttribute('value') == 'Update/Refresh':
                        input.click()
                        break
            else:
                raise RuntimeError('could not find submit button for %s' % filename)

    def addGroup(self, name):
        if not self.navigate('https://sourceforge.net/projects/%s/develop' % self.__projectName):
            raise RuntimeError('Could not go to project page')

        bugs = self.findElement('a', 'innerText', 'Bugs')
        if bugs is None:
            raise RuntimeError('Could not go to bugs tracker')
        bugs.click()

        if not self.clickLink('Admin'):
            raise RuntimeError('Could not go to tracker admin')

        # Collect admin links for all trackers

        links = []
        for link in self.getElementsList('a'):
            if link.getAttribute('href').find('/tracker/admin/?atid=') != -1:
                links.append(link.getAttribute('href'))

        # Add group to all trackers

        for link in links:
            self.navigate(link)

            if not self.clickLink('Add/Update Groups'):
                raise RuntimeError('Could not go to group add form')

            if not self.setTextBox('name', name):
                raise RuntimeError('Could not fill name')

            submit = self.findElement('input', 'name', 'post_changes')
            if submit is None:
                raise RuntimeError('Where is the submit button ?')
            submit.click()


def main():
    sf = SourceForge('pydropbar')
    sf.login('fraca7', file('.passwd', 'rb').read().strip())

    sf.addRelease('test')
    sf.editRelease1('notes', 'changes', ['foobar-1.0.tar.gz', 'foobar-1.0.exe'])
    sf.editRelease2([('appbar-1.0.tar.gz', 'Platform-Independent', 'Source .gz'),
                     ('foobar-1.0.exe', 'i386', '.exe')])

    sf.addGroup('TestGroup')

    sf.logout()
    sf.quit()


if __name__ == '__main__':
    main()