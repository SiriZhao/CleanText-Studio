#ifndef AppVersion
  #define AppVersion "1.3.1"
#endif
[Setup]
AppId={{A8A01C8C-7B35-4F18-9C14-72CAEE75A811}
AppName=CleanText Studio
AppVersion={#AppVersion}
AppPublisher=SiriZhao
DefaultDirName={localappdata}\Programs\CleanText Studio
DefaultGroupName=CleanText Studio
OutputDir=dist\release
OutputBaseFilename=CleanText-Studio-v{#AppVersion}-Windows-x64-Setup
PrivilegesRequired=lowest
SetupIconFile=assets\icon.ico
Compression=lzma2
SolidCompression=yes
UninstallDisplayIcon={app}\CleanText Studio.exe
[Tasks]
Name: desktopicon; Description: "创建桌面快捷方式"; Flags: unchecked
[Files]
Source: "dist\CleanText Studio\*"; DestDir: "{app}"; Flags: recursesubdirs
[Icons]
Name: "{group}\CleanText Studio"; Filename: "{app}\CleanText Studio.exe"
Name: "{autodesktop}\CleanText Studio"; Filename: "{app}\CleanText Studio.exe"; Tasks: desktopicon
