'''
Task Coach - Your friendly task manager
Copyright (C) 2004-2009 Frank Niessink <frank@niessink.com>

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

import observer


class Composite(object):
    def __init__(self, children=None, parent=None):
        super(Composite, self).__init__()
        self.__parent = parent
        self.__children = children or []
        for child in self.__children:
            child.setParent(self)
        
    def __getstate__(self):
        return dict(children=self.__children[:], 
                    parent=self.__parent)
    
    def __setstate__(self, state):
        self.__parent = state['parent']
        self.__children = state['children']

    def __getcopystate__(self):
        ''' Return the information needed to create a copy as a dict. '''
        try:
            state = super(Composite, self).__getcopystate__()
        except AttributeError:
            state = dict()
        state.update(dict(children=[child.copy() for child in self.__children], 
                          parent=self.__parent))
        return state
    
    def parent(self):
        return self.__parent
    
    def ancestors(self):
        ''' Return the parent, and its parent, etc., as a list. '''
        parent = self.parent()
        return parent.ancestors() + [parent] if parent else []
    
    def family(self):
        ''' Return this object, its ancestors and all of its children 
            (recursively). '''
        return self.ancestors() + [self] + self.children(recursive=True)
    
    def setParent(self, parent):
        self.__parent = parent
    
    def children(self, recursive=False):
        if recursive:
            result = self.__children[:]
            for child in self.__children:
                result.extend(child.children(recursive=True))
            return result
        else:
            return self.__children

    def copy(self, *args, **kwargs):
        kwargs['parent'] = self.parent()
        kwargs['children'] = [child.copy() for child in self.children()]
        return self.__class__(*args, **kwargs)
        
    def newChild(self, *args, **kwargs):
        kwargs['parent'] = self
        return self.__class__(*args, **kwargs)
    
    def addChild(self, child):
        self.__children.append(child)
        child.setParent(self)
        
    def removeChild(self, child):
        self.__children.remove(child)
        # We don't reset the parent of the child, because that makes restoring
        # the parent-child relationship easier.
    
    # FIXME: this is for do/undo, need a better, generic, implementation
    def replaceChildren(self, children): 
        self.__children = children
    
    def replaceParent(self, parent):
        self.__parent = parent
        

class ObservableComposite(Composite):
    def __setstate__(self, state, event=None):
        notify = event is None
        event = event or patterns.Event()
        oldChildren = self.children()[:]
        super(ObservableComposite, self).__setstate__(state)
        if oldChildren:
            self.removeChildEvent(event, *oldChildren)
        if self.children():
            self.addChildEvent(event, *self.children())
        if notify:
            event.send()

    def addChild(self, child, event=None):
        notify = event is None
        event = event or observer.Event()
        super(ObservableComposite, self).addChild(child)
        self.addChildEvent(event, child)
        if notify:
            event.send()

    def addChildEvent(self, event, *children):
        event.addSource(self, *children, **dict(type=self.addChildEventType()))

    @classmethod
    def addChildEventType(class_):
        return 'composite(%s).child.add'%class_

    def removeChild(self, child, event=None):
        notify = event is None
        event = event or observer.Event()
        super(ObservableComposite, self).removeChild(child)
        self.removeChildEvent(event, child)
        if notify:
            event.send()

    def removeChildEvent(self, event, *children):    
        event.addSource(self, *children, **dict(type=self.removeChildEventType()))

    @classmethod
    def removeChildEventType(class_):
        return 'composite(%s).child.remove'%class_
    
    def replaceChildren(self, children, event=None):
        if children == self.children():
            return
        notify = event is None
        event = event or observer.Event()
        oldChildren = self.children()[:]
        super(ObservableComposite, self).replaceChildren(children)
        if oldChildren:
            self.removeChildEvent(event, *oldChildren)
        if children: 
            self.addChildEvent(event, *children)
        if notify:
            event.send()
        
    @classmethod
    def modificationEventTypes(class_):
        try:
            eventTypes = super(ObservableComposite, class_).modificationEventTypes()
        except AttributeError:
            eventTypes = []
        return eventTypes + [class_.addChildEventType(), 
                             class_.removeChildEventType()]
            

class CompositeCollection(object):
    def __init__(self, initList=None, *args, **kwargs):
        super(CompositeCollection, self).__init__(*args, **kwargs)
        self.extend(initList or [])
    
    def append(self, composite, event=None):
        return self.extend([composite], event)

    def extend(self, composites, event=None):
        if not composites:
            return
        notify = event is None
        event = event or observer.Event()
        compositesAndAllChildren = self._compositesAndAllChildren(composites) 
        super(CompositeCollection, self).extend(compositesAndAllChildren, event)
        parentsWithChildrenAdded = self._addCompositesToParent(composites, event)
        if notify:
            event.send()
            
    def _compositesAndAllChildren(self, composites):
        compositesAndAllChildren = set(composites) 
        for composite in composites:
            compositesAndAllChildren |= set(composite.children(recursive=True))
        return list(compositesAndAllChildren)

    def _addCompositesToParent(self, composites, event):
        parents = {}
        for composite in composites:
            parent = composite.parent()
            if parent and parent in self and composite not in parent.children():
                parent.addChild(composite, event)
                if parent not in composites:
                    parents.setdefault(parent, []).append(composite)
        return parents
    
    def remove(self, composite, event=None):
        return self.removeItems([composite], event) if composite in self else event

    def removeItems(self, composites, event=None):
        if not composites:
            return
        notify = event is None
        event = event or observer.Event()
        compositesAndAllChildren = self._compositesAndAllChildren(composites)
        super(CompositeCollection, self).removeItems(compositesAndAllChildren, event)
        self._removeCompositesFromParent(composites, event)
        if notify:
            event.send()

    def _removeCompositesFromParent(self, composites, event):
        for composite in composites:
            parent = composite.parent()
            if parent:
                parent.removeChild(composite, event)
                            
    def rootItems(self):
        return [composite for composite in self if composite.parent() is None or \
                composite.parent() not in self]                                            


class CompositeSet(CompositeCollection, observer.ObservableSet):
    pass

    
class CompositeList(CompositeCollection, observer.ObservableList):
    pass

