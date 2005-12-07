iconlist = [
('copy', 'actions', 'editcopy', [16, 22, 32]),
('cut', 'actions', 'editcut', [16, 22, 32]),
('delete', 'actions', 'editdelete', [16, 22, 32]),
('edit', 'actions', 'edit', [16, 22, 32]),
('fileopen', 'actions', 'fileopen', [16, 22, 32]),
('close', 'actions', 'fileclose', [16]),
('exit', 'actions', 'exit', [16]),
('help', 'actions', 'help', [16]),
('info', 'actions', 'messagebox_info', [16]),
('markcompleted', 'apps', 'korganizer_todo', [16, 22, 32]),
('new', 'actions', 'filenew', [16, 22, 32]),
('on', 'actions', 'apply', [16]),
('paste', 'actions', 'editpaste', [16, 22, 32]),
('undo', 'actions', 'undo', [16, 22, 32]),
('redo', 'actions', 'redo', [16, 22, 32]),
('save', 'actions', 'filesave', [16, 22, 32]),
('saveas', 'actions', 'filesaveas', [16]),
('task', 'actions', 'ledblue', [16]),
('task_completed', 'actions', 'ledgreen', [16]),
('task_duetoday', 'actions', 'ledorange', [16]),
('task_inactive', 'actions', 'ledgrey', [16]),
('task_overdue', 'actions', 'ledred', [16]),
('taskcoach', 'apps', 'korganizer_todo', [16, 22, 32]),
('tasks', 'filesystems', 'folder_blue', [16]),
('tasks_open', 'filesystems', 'folder_blue_open', [16]),
('tasks_completed', 'filesystems', 'folder_green', [16]),
('tasks_completed_open', 'filesystems', 'folder_green_open', [16]),
('tasks_duetoday', 'filesystems', 'folder_orange', [16]),
('tasks_duetoday_open', 'filesystems', 'folder_orange_open', [16]),
('tasks_inactive', 'filesystems', 'folder_grey', [16]),
('tasks_inactive_open', 'filesystems', 'folder_grey_open', [16]),
('tasks_overdue', 'filesystems', 'folder_red', [16]),
('tasks_overdue_open', 'filesystems', 'folder_red_open', [16]),
('listview', 'actions', 'view_detailed', [16, 22, 32]),
('treeview', 'actions', 'view_tree', [16, 22, 32]),
('start', 'actions', 'history', [16, 22, 32]),
('stop', 'actions', 'history_clear', [16, 22, 32]),
('tick', 'apps', 'clock', [16]),
('tack', 'apps', 'ktimer', [16]),
('date', 'apps', 'date', [16, 22, 32]),
('description', 'actions', 'pencil', [16, 22, 32]),
('restore', 'apps', 'kcmkwm', [16]),
('budget', 'apps', 'kcalc', [16, 22, 32]),
('viewalltasks', 'apps', 'kreversi', [16]),
('viewexpand', 'actions', 'edit_add', [16]),
('viewcollapse', 'actions', 'edit_remove', [16]),
('configure', 'actions', 'configure', [16]),
('language', 'apps', 'edu_languages', [22]),
('ascending', 'actions', 'up', [16]),
('descending', 'actions', 'down', [16]),
('category', 'filesystems', 'folder_download', [16, 22]),
('revenue', 'apps', 'kchart', [22, 32]),
('colorize', 'actions', 'colorize', [22]),
('windows', 'apps', 'window_list', [22]),
('email', 'apps', 'email', [16])]

icons = {}

for pngName, type, filename, sizes in iconlist:
    for size in sizes:
        size = '%dx%d'%(size, size)
        icons['%s%s'%(pngName, size)] = 'nuvola/%s/%s/%s.png'%(size, type, filename)

