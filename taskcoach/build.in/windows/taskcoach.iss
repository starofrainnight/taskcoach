; Task Coach - Your friendly task manager
; Copyright (C) 2004-2008 Frank Niessink <frank@niessink.com>
; 
; Task Coach is free software: you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; (at your option) any later version.
; 
; Task Coach is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.
; 
; You should have received a copy of the GNU General Public License
; along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
; Inno Setup Script

[Setup]
AppName=%(name)s
AppVerName=%(name)s %(version)s
AppPublisher=%(author)s
AppPublisherURL=%(url)s
AppSupportURL=%(url)s
AppUpdatesURL=%(url)s
DefaultDirName={pf}\%(filename)s
DefaultGroupName=%(name)s
AllowNoIcons=yes
LicenseFile=../LICENSE.txt
Compression=lzma
SolidCompression=yes
OutputDir=../dist
OutputBaseFilename=%(filename)s-%(version)s-win32
ChangesAssociations=yes 
WizardImageFile=..\icons.in\splash_inno.bmp
PrivilegesRequired=none

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: associate; Description: "{cm:AssocFileExtension,{app},.tsk}"; GroupDescription: "Other tasks:"; Flags: unchecked
Name: userstartup; Description: "Run %(name)s everytime Windows is started"; GroupDescription: "Other tasks:"; Flags: unchecked

[Files]
Source: "%(filename)s-%(version)s-win32exe\%(filename)s.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(filename)s-%(version)s-win32exe\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "..\templates\*.tsktmpl"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[INI]
Filename: "{app}\%(filename)s.url"; Section: "InternetShortcut"; Key: "URL"; String: "%(url)s"

[Registry]
Root: HKCR; Subkey: ".tsk"; ValueType: string; ValueName: ""; ValueData: "TaskCoach"; Flags: uninsdeletevalue; Check: IsAdminLoggedOn
Root: HKCR; Subkey: "TaskCoach"; ValueType: string; ValueName: ""; ValueData: "%(name)s File"; Flags: uninsdeletekey; Check: IsAdminLoggedOn
Root: HKCR; Subkey: "TaskCoach\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\%(filename)s.EXE,0"; Check: IsAdminLoggedOn
Root: HKCR; Subkey: "TaskCoach\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\%(filename)s.EXE"" ""%%1"""; Check: IsAdminLoggedOn
Root: HKCU; Subkey: "Software\Classes\.tsk"; ValueType: string; ValueName: ""; ValueData: "TaskCoachFile"; Flags: uninsdeletevalue; Check: not IsAdminLoggedOn
Root: HKCU; Subkey: "Software\Classes\TaskCoachFile"; ValueType: string; ValueName: ""; ValueData: "%(name)s File"; Flags: uninsdeletekey; Check: not IsAdminLoggedOn
Root: HKCU; Subkey: "Software\Classes\TaskCoachFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\%(filename)s.EXE,0"; Check: not IsAdminLoggedOn
Root: HKCU; Subkey: "Software\Classes\TaskCoachFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\%(filename)s.EXE"" ""%%1"""; Check: not IsAdminLoggedOn

[Icons]
Name: "{group}\%(name)s"; Filename: "{app}\%(filename)s.exe"; WorkingDir: "{app}"
Name: "{group}\{cm:ProgramOnTheWeb,%(name)s}"; Filename: "{app}\%(filename)s.url"
Name: "{group}\{cm:UninstallProgram,%(name)s}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\%(name)s"; Filename: "{app}\%(filename)s.exe"; Tasks: desktopicon; WorkingDir: "{app}"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\%(name)s"; Filename: "{app}\%(filename)s.exe"; Tasks: quicklaunchicon; WorkingDir: "{app}"
Name: "{userstartup}\%(name)s"; Filename: "{app}\%(filename)s.exe"; Tasks: userstartup

[Run]
Filename: "{app}\%(filename)s.exe"; Description: "{cm:LaunchProgram,%(name)s}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\%(filename)s.url"

