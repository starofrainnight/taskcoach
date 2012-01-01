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

from taskcoachlib import patterns
from taskcoachlib.domain import base
import task


class Sorter(base.TreeSorter):
    DomainObjectClass = task.Task # What are we sorting
    TaskStatusAttributes = ('plannedStartDateTime', 'completionDateTime',
                            'prerequisites')
    
    def __init__(self, *args, **kwargs):
        self.__treeMode = kwargs.pop('treeMode', False)
        self.__sortByTaskStatusFirst = kwargs.pop('sortByTaskStatusFirst', True)
        super(Sorter, self).__init__(*args, **kwargs)
        for attribute in self.TaskStatusAttributes:
            try:
                eventType = getattr(self.DomainObjectClass, '%sChangedEventType' % attribute)()
            except AttributeError:
                eventType = 'task.%s' % attribute
            patterns.Publisher().registerObserver(self.onAttributeChanged, 
                                                  eventType=eventType)
    
    @patterns.eventSource       
    def setTreeMode(self, treeMode=True, event=None):
        self.__treeMode = treeMode
        try:
            self.observable().setTreeMode(treeMode)
        except AttributeError:
            pass
        self.reset(event=event)
        event.addSource(self, type=self.sortEventType()) # force notification 

    def treeMode(self):
        return self.__treeMode
                
    def sortByTaskStatusFirst(self, sortByTaskStatusFirst):
        self.__sortByTaskStatusFirst = sortByTaskStatusFirst
        # We don't need to invoke self.reset() here since when this property is
        # changed, the sort order also changes which in turn will cause 
        # self.reset() to be called.
                                
    def createSortKeyFunction(self):
        statusSortKey = self.__createStatusSortKey()
        regularSortKey = super(Sorter, self).createSortKeyFunction()
        return lambda task: statusSortKey(task) + [regularSortKey(task)]

    def __createStatusSortKey(self):
        if self.__sortByTaskStatusFirst:
            if self._sortAscending:
                return lambda task: [task.completed(), task.inactive()]
            else:
                return lambda task: [not task.completed(), not task.inactive()]
        else:
            return lambda task: []

    def _registerObserverForAttribute(self, attribute):
        # Sorter is always observing completion date, planned start date and 
        # prerequisites because sorting by status depends on those attributes. 
        # Hence we don't need to subscribe to these attributes when they become 
        # the sort key.
        if attribute not in self.TaskStatusAttributes:
            super(Sorter, self)._registerObserverForAttribute(attribute)
            
    def _removeObserverForAttribute(self, attribute):
         # See comment at _registerObserverForAttribute.
        if attribute not in self.TaskStatusAttributes:
            super(Sorter, self)._removeObserverForAttribute(attribute)
        
