#!/usr/bin/env python

"""
Task Coach - Your friendly task manager
Copyright (C) 2004-2016 Task Coach developers <developers@taskcoach.org>

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
"""

import os
import sys
import inspect
from collections import namedtuple

# Workaround for a bug in Ubuntu 10.10
os.environ["XLIB_SKIP_ARGB_VISUALS"] = "1"

try:
    inspect.getargspec
except AttributeError:
    ArgSpec = namedtuple("ArgSpec", "args varargs keywords defaults")

    # Workaround for getargspec() missing inspect.getargspec() for python3.11 or later
    def getargspec(func):
        """Get the names and default values of a function's parameters.

        A tuple of four things is returned: (args, varargs, keywords, defaults).
        'args' is a list of the argument names, including keyword-only argument names.
        'varargs' and 'keywords' are the names of the * and ** parameters or None.
        'defaults' is an n-tuple of the default values of the last n parameters.

        This function is deprecated, as it does not support annotations or
        keyword-only parameters and will raise ValueError if either is present
        on the supplied callable.

        For a more structured introspection API, use inspect.signature() instead.

        Alternatively, use getfullargspec() for an API with a similar namedtuple
        based interface, but full support for annotations and keyword-only
        parameters.

        Deprecated since Python 3.5, use `inspect.getfullargspec()`.
        """
        from inspect import getfullargspec

        args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, ann = (
            getfullargspec(func)
        )
        if kwonlyargs or ann:
            raise ValueError(
                "Function has keyword-only parameters or annotations"
                ", use inspect.signature() API which can support them"
            )
        return ArgSpec(args, varargs, varkw, defaults)

    inspect.getargspec = getargspec

# This prevents a message printed to the console when wx.lib.masked
# is imported from taskcoachlib.widgets on Ubuntu 12.04 64 bits...
try:
    from mx import DateTime
except ImportError:
    pass


if not hasattr(sys, "frozen"):
    # These checks are only necessary in a non-frozen environment, i.e. we
    # skip these checks when run from a py2exe-fied application
    try:
        import wxversion

        wxversion.select(["2.8-unicode", "3.0"], optionsRequired=True)
    except ImportError:
        # There is no wxversion for py3
        pass

    try:
        import taskcoachlib  # pylint: disable=W0611
    except ImportError:
        # On Ubuntu 12.04, taskcoachlib is installed in /usr/share/pyshared,
        # but that folder is not on the python path. Don't understand why.
        # We'll add it manually so the application can find it.
        sys.path.insert(0, "/usr/share/pyshared")
        try:
            import taskcoachlib  # pylint: disable=W0611
        except ImportError:
            sys.stderr.write(
                """ERROR: cannot import the library 'taskcoachlib'.
Please see https://answers.launchpad.net/taskcoach/+faq/1063 
for more information and possible resolutions.
"""
            )
            sys.exit(1)


def start():
    """Process command line options and start the application."""

    # pylint: disable=W0404
    from taskcoachlib import config, application

    options, args = config.ApplicationOptionParser().parse_args()
    app = application.Application(options, args)
    if options.profile:
        import cProfile

        cProfile.runctx(
            "app.start()", globals(), locals(), filename=".profile"
        )
    else:
        app.start()


if __name__ == "__main__":
    start()
