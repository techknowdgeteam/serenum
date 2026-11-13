Option Explicit
Dim fso, shell, baseDir, updaterFile, pythonw, localAppData, pathValue, entries, item
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")
baseDir = fso.GetParentFolderName(WScript.ScriptFullName)
updaterFile = fso.BuildPath(baseDir, "serenum_updater.pyw")
If Not fso.FileExists(updaterFile) Then
    MsgBox "The Serenum updater is missing. Reinstall Serenum using the complete installer ZIP.", vbCritical, "Update Serenum"
    WScript.Quit 2
End If
pythonw = ""
localAppData = shell.ExpandEnvironmentStrings("%LOCALAPPDATA%")
If fso.FileExists("C:\Program Files\Python310\pythonw.exe") Then pythonw = "C:\Program Files\Python310\pythonw.exe"
If pythonw = "" And localAppData <> "%LOCALAPPDATA%" Then
    If fso.FileExists(localAppData & "\Programs\Python\Python310\pythonw.exe") Then pythonw = localAppData & "\Programs\Python\Python310\pythonw.exe"
End If
If pythonw = "" And fso.FileExists("C:\Program Files\Python311\pythonw.exe") Then pythonw = "C:\Program Files\Python311\pythonw.exe"
If pythonw = "" And fso.FileExists("C:\Program Files\Python312\pythonw.exe") Then pythonw = "C:\Program Files\Python312\pythonw.exe"
If pythonw = "" And localAppData <> "%LOCALAPPDATA%" Then
    If fso.FileExists(localAppData & "\Programs\Python\Python311\pythonw.exe") Then pythonw = localAppData & "\Programs\Python\Python311\pythonw.exe"
    If pythonw = "" And fso.FileExists(localAppData & "\Programs\Python\Python312\pythonw.exe") Then pythonw = localAppData & "\Programs\Python\Python312\pythonw.exe"
End If
If pythonw = "" Then
    MsgBox "Python 3.10, 3.11 or 3.12 with Tcl/Tk could not be found. Install or repair Python, then retry.", vbExclamation, "Update Serenum"
    WScript.Quit 3
End If
shell.CurrentDirectory = baseDir
shell.Run Chr(34) & pythonw & Chr(34) & " " & Chr(34) & updaterFile & Chr(34), 0, False
