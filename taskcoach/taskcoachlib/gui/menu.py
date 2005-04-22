import wx, uicommand
   
class Menu(wx.Menu, uicommand.UICommandContainer):
    def __init__(self, window):
        super(Menu, self).__init__()
        self._window = window

    def __len__(self):
        return self.GetMenuItemCount()

    def appendUICommand(self, uiCommand):
        uiCommand.appendToMenu(self, self._window)    
    
    def appendMenu(self, text, subMenu):
        subMenuItem = wx.MenuItem(self, -1, text, subMenu=subMenu)
        # hack to force a 16 bit margin. SetMarginWidth doesn't work
        if '__WXMSW__' in wx.PlatformInfo:
            subMenuItem.SetBitmap(wx.ArtProvider_GetBitmap('nobitmap', wx.ART_MENU, (16,16)))
        self.AppendItem(subMenuItem)


class MainMenu(wx.MenuBar):
    def __init__(self, mainwindow, uiCommands):
        super(MainMenu, self).__init__()
        self.Append(FileMenu(mainwindow, uiCommands), '&File')
        self.Append(EditMenu(mainwindow, uiCommands), '&Edit')
        self.Append(ViewMenu(mainwindow, uiCommands), '&View')
        self.Append(TaskMenu(mainwindow, uiCommands), '&Task')
        self.Append(EffortMenu(mainwindow, uiCommands), 'Eff&ort')
        self.Append(HelpMenu(mainwindow, uiCommands), '&Help')


class FileMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(FileMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['open', 'merge', 'close', None, 
            'save', 'saveas', 'saveselection', None, 'quit'])


class EditMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(EditMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['undo', 'redo', None, 'cut', 
            'copy', 'paste', 'pasteassubtask', None])
        self.appendMenu('Select', SelectMenu(mainwindow, uiCommands))
        

class SelectMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(SelectMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['selectall', 'selectcompleted', 
            None, 'invertselection', 'clearselection'])


class ViewMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(ViewMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['viewalltasks'])
        self.appendMenu('Tasks that are', 
            ViewTaskStatesMenu(mainwindow, uiCommands))
        self.appendMenu('Tasks due before end of',
            ViewTasksByDueDateMenu(mainwindow, uiCommands))
        self.appendUICommands(uiCommands, [None])
        self.appendMenu('In the task list', 
            ViewTaskListMenu(mainwindow, uiCommands))
        self.appendMenu('In the task tree', 
            ViewTaskTreeMenu(mainwindow, uiCommands))
        self.appendUICommands(uiCommands, [None])
        self.appendMenu('&Toolbar', ToolBarMenu(mainwindow, uiCommands))        
        self.appendUICommands(uiCommands, ['viewfinddialog', 'viewstatusbar', 
            'viewsplashscreen'])   

           
class ViewTaskStatesMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(ViewTaskStatesMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['viewactivetasks',
            'viewinactivetasks', 'viewcompletedtasks', None,
            'viewoverduetasks', 'viewoverbudgettasks'])

                
class ViewTaskListMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(ViewTaskListMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['viewstartdate',
            'viewduedate', 'viewdaysleft', 'viewcompletiondate',
            'viewbudget', 'viewtotalbudget', 'viewtimespent',
            'viewtotaltimespent', 'viewbudgetleft', 'viewtotalbudgetleft',
            None, 'viewcompositetasks'])
 
           
class ViewTaskTreeMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(ViewTaskTreeMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['viewexpandall', 'viewcollapseall'])

        
    
class ToolBarMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(ToolBarMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['toolbarhide', 'toolbarsmall',
            'toolbarmedium', 'toolbarbig'])


class ViewTasksByDueDateMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(ViewTasksByDueDateMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['viewdueunlimited', 'viewduetoday',
            'viewduetomorrow', 'viewdueworkweek', 'viewdueweek',
            'viewduemonth', 'viewdueyear'])


class TaskMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(TaskMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['new', 'newsubtask', 
            None, 'edit', 'markcompleted', None, 'delete'])
            
            
class EffortMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(EffortMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['neweffort', 'editeffort', 'deleteeffort', None, 
            'starteffort', 'starteffortadjacent', 'stopeffort'])
        
        
class HelpMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(HelpMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['helptasks', 'helpcolors', None, 
            'about', 'license'])


class TaskBarMenu(Menu):
    def __init__(self, taskBarIcon, uiCommands):
        super(TaskBarMenu, self).__init__(taskBarIcon)
        self.appendUICommands(uiCommands, ['new', 'stopeffort', None, 'restore', 'quit'])


class TaskPopupMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(TaskPopupMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['cut', 'copy', 'paste',
            'pasteassubtask', None, 'new', 'newsubtask', None, 'edit', 
            'markcompleted', None, 'delete', None, 'neweffort', 'starteffort',
            'starteffortadjacent', 'stopeffort'])


class EffortPopupMenu(Menu):
    def __init__(self, mainwindow, uiCommands, effortList, effortViewer):
        super(EffortPopupMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['new', None, 'editeffort', 'deleteeffort',
            None, 'stopeffort'])
