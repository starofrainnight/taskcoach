'''
Task Coach - Your friendly task manager
Copyright (C) 2004-2012 Task Coach developers <developers@taskcoach.org>

Task Coach is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Task Coach is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from taskcoachlib import patterns, command
from taskcoachlib.domain import task
from CommandTestCase import CommandTestCase


    
class DeleteCommandTest(CommandTestCase):
    def setUp(self):
        super(DeleteCommandTest, self).setUp()
        self.item = 'Item'
        self.items = patterns.List([self.item])
        
    def deleteItem(self, items=None):
        delete = command.DeleteCommand(self.items, items or [])
        delete.do()
        
    def testDeleteItem_WithoutSelection(self):
        self.deleteItem()
        self.assertDoUndoRedo(lambda: self.assertEqual([self.item], self.items))
        
    def testDeleteItem_WithSelection(self):
        self.deleteItem([self.item])
        self.assertDoUndoRedo(lambda: self.assertEqual([], self.items),
                              lambda: self.assertEqual([self.item], self.items))

    def testItemsAreNotNew(self):
        self.failIf(command.DeleteCommand(self.items, []).itemsAreNew())


class EditSubjectTestCase(CommandTestCase):
    ItemClass = task.Task
    ContainerClass = task.TaskList
    
    def setUp(self):
        super(EditSubjectTestCase, self).setUp()
        self.item1 = self.ItemClass(subject='item1')
        self.item2 = self.ItemClass(subject='item2')
        self.container = self.ContainerClass([self.item1, self.item2])
        
    def editSubject(self, newSubject, *items):
        editSubjectCommand = command.EditSubjectCommand(self.container, 
                                                        items, 
                                                        newValue=newSubject)
        editSubjectCommand.do()
        
    def testEditSubject(self):
        self.editSubject('new', self.item1)
        self.assertDoUndoRedo(lambda: self.assertEqual('new', self.item1.subject()),
                              lambda: self.assertEqual('item1', self.item1.subject()))
        
    def testEditMultipleSubjects(self):
        self.editSubject('new', self.item1, self.item2)
        self.assertDoUndoRedo(lambda: self.assertEqual('newnew', 
                                      self.item1.subject() + self.item2.subject()),
                              lambda: self.assertEqual('item1item2', 
                                      self.item1.subject() + self.item2.subject()))

    def testItemsAreNotNew(self):
        self.failIf(command.EditSubjectCommand(self.container, [], 
                                               newValue='New subject').itemsAreNew())

