Option Explicit

Dim fso, shell, baseDir, setupFile, pythonw, localAppData, pathValue, entries, item
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

baseDir = fso.GetParentFolderName(WScript.ScriptFullName)
setupFile = fso.BuildPath(baseDir, "serenum_setup.pyw")

If Not fso.FileExists(setupFile) Then
    MsgBox "Serenum setup file is missing." & vbCrLf & _
           "Please extract the complete Serenum package, then open Start_Serenum.vbs again.", _
           vbCritical, "Serenum"
    WScript.Quit 2
End If

pythonw = ""
localAppData = shell.ExpandEnvironmentStrings("%LOCALAPPDATA%")

' Prefer the Python 3.10 installation already used by Serenum.
If fso.FileExists("C:\Program Files\Python310\pythonw.exe") Then
    pythonw = "C:\Program Files\Python310\pythonw.exe"
End If

' Check standard per-user and machine-wide Python installations.
If pythonw = "" And localAppData <> "%LOCALAPPDATA%" Then
    If fso.FileExists(localAppData & "\Programs\Python\Python310\pythonw.exe") Then
        pythonw = localAppData & "\Programs\Python\Python310\pythonw.exe"
    End If
End If

If pythonw = "" Then
    If fso.FileExists("C:\Program Files\Python311\pythonw.exe") Then pythonw = "C:\Program Files\Python311\pythonw.exe"
End If
If pythonw = "" Then
    If fso.FileExists("C:\Program Files\Python312\pythonw.exe") Then pythonw = "C:\Program Files\Python312\pythonw.exe"
End If
If pythonw = "" And localAppData <> "%LOCALAPPDATA%" Then
    If fso.FileExists(localAppData & "\Programs\Python\Python311\pythonw.exe") Then
        pythonw = localAppData & "\Programs\Python\Python311\pythonw.exe"
    End If
End If
If pythonw = "" And localAppData <> "%LOCALAPPDATA%" Then
    If fso.FileExists(localAppData & "\Programs\Python\Python312\pythonw.exe") Then
        pythonw = localAppData & "\Programs\Python\Python312\pythonw.exe"
    End If
End If

' Last attempt: look for pythonw.exe in the user's PATH.
If pythonw = "" Then
    pathValue = shell.ExpandEnvironmentStrings("%PATH%")
    entries = Split(pathValue, ";")
    For Each item In entries
        item = Replace(item, Chr(34), "")
        If Len(Trim(item)) > 0 Then
            If fso.FileExists(fso.BuildPath(Trim(item), "pythonw.exe")) Then
                pythonw = fso.BuildPath(Trim(item), "pythonw.exe")
                Exit For
            End If
        End If
    Next
End If

If pythonw = "" Then
    MsgBox "A supported Python 3.10, 3.11 or 3.12 installation could not be found." & vbCrLf & _
           "Install Python for Windows with the Tcl/Tk option enabled, then run this launcher again.", _
           vbExclamation, "Serenum setup"
    WScript.Quit 3
End If

shell.CurrentDirectory = baseDir
' Window style 0 keeps Python and all setup subprocesses hidden from the desktop.
shell.Run Chr(34) & pythonw & Chr(34) & " " & Chr(34) & setupFile & Chr(34), 0, False
