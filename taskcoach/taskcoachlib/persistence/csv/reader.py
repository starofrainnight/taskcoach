'''
Task Coach - Your friendly task manager
Copyright (C) 2011 Task Coach developers <developers@taskcoach.org>

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

from taskcoachlib.thirdparty.dateutil import parser as dparser
from taskcoachlib.i18n import _
from taskcoachlib.domain.category import Category
from taskcoachlib.domain.task import Task
from taskcoachlib.domain.date import DateTime

import csv, tempfile, StringIO


class CSVReader(object):
    def __init__(self, taskList, categoryList):
        self.taskList = taskList
        self.categoryList = categoryList

    def read(self, **kwargs):
        fp = tempfile.TemporaryFile()
        fp.write(file(kwargs['filename'], 'rb').read().decode(kwargs['encoding']).encode('UTF-8'))
        fp.seek(0)

        # When fields are associated with categories, create a top-level category for the
        # field and a subcategory for each possible value.

        toplevelCategories = dict()
        for idx, headerName in enumerate(kwargs['fields']):
            if kwargs['mappings'][idx] == _('Category'):
                category = Category(subject=headerName)
                toplevelCategories[headerName] = (category, dict())
                self.categoryList.append(category)

        reader = csv.reader(fp, dialect=kwargs['dialect'])
        if kwargs['hasHeaders']:
            reader.next()

        tasksById = dict()
        tasks = []

        for line in reader:
            subject = _('No subject')
            id_ = None
            description = StringIO.StringIO()
            categories = []
            priority = 0
            startDate = None
            dueDate = None
            completionDate = None

            for idx, fieldValue in enumerate(line):
                if kwargs['mappings'][idx] == _('ID'):
                    id_ = fieldValue.decode('UTF-8')
                elif kwargs['mappings'][idx] == _('Subject'):
                    subject = fieldValue.decode('UTF-8')
                elif kwargs['mappings'][idx] == _('Description'):
                    description.write(fieldValue.decode('UTF-8'))
                    description.write(u'\n')
                elif kwargs['mappings'][idx] == _('Category') and fieldValue:
                    name = fieldValue.decode('UTF-8')
                    parent, cats = toplevelCategories[kwargs['fields'][idx]]
                    if name in cats:
                        categories.append(cats[name])
                    else:
                        newCat = Category(subject=name)
                        parent.addChild(newCat)
                        cats[name] = newCat
                        self.categoryList.append(newCat)
                    toplevelCategories[kwargs['fields'][idx]] = (parent, cats)
                elif kwargs['mappings'][idx] == _('Priority'):
                    try:
                        priority = int(fieldValue)
                    except ValueError:
                        pass
                elif kwargs['mappings'][idx] == _('Start date'):
                    if fieldValue != '':
                        try:
                            startDate = dparser.parse(fieldValue.decode('UTF-8'), fuzzy=True).replace(tzinfo=None)
                            startDate = DateTime(startDate.year, startDate.month, startdate.day, 0, 0, 0)
                        except:
                            pass
                elif kwargs['mappings'][idx] == _('Due date'):
                    if fieldValue != '':
                        try:
                            dueDate = dparser.parse(fieldValue.decode('UTF-8'), fuzzy=True).replace(tzinfo=None)
                            dueDate = DateTime(dueDate.year, dueDate.month, dueDate.day, 23, 59, 0)
                        except:
                            pass
                elif kwargs['mappings'][idx] == _('Completion date'):
                    if fieldValue != '':
                        try:
                            completionDate = dparser.parse(fieldValue.decode('UTF-8'), fuzzy=True).replace(tzinfo=None)
                            completionDate = DateTime(completionDate.year, completionDate.month, completionDate.day, 12, 0, 0)
                        except:
                            pass

            task = Task(subject=subject,
                        description=description.getvalue(),
                        priority=priority,
                        startDateTime=startDate,
                        dueDateTime=dueDate,
                        completionDateTime=completionDate)

            if id_ is not None:
                tasksById[id_] = task

            for category in categories:
                category.addCategorizable(task)
                task.addCategory(category)

            tasks.append(task)

        # OmniFocus uses the task's ID to keep track of hierarchy: 1 => 1.1 and 1.2, etc...

        if tasksById:
            ids = []
            for id_, task in tasksById.items():
                try:
                    ids.append(tuple(map(int, id_.split('.'))))
                except ValueError:
                    self.taskList.append(task)

            ids.sort()
            ids.reverse()

            for id_ in ids:
                sid = '.'.join(map(str, id_))
                if len(id_) >= 2:
                    pid = '.'.join(map(str, id_[:-1]))
                    if pid in tasksById:
                        tasksById[pid].addChild(tasksById[sid])
                else:
                    self.taskList.append(tasksById[sid])
        else:
            self.taskList.extend(tasks)