Option Explicit
Dim fso, shell, baseDir, targetFile, pythonExe, pythonw, version, localAppData
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")
baseDir = fso.GetParentFolderName(WScript.ScriptFullName)
targetFile = fso.BuildPath(baseDir, "serenum_setup.pyw")
If Not fso.FileExists(targetFile) Then
    MsgBox "Serenum setup is missing. Run Install_Serenum.vbs from the complete installer package.", vbCritical, "Serenum setup"
    WScript.Quit 2
End If

pythonExe = ""
pythonw = ""
localAppData = shell.ExpandEnvironmentStrings("%LOCALAPPDATA%")

' Ask the Windows Python Launcher for a specific supported runtime.
For Each version In Array("3.12", "3.11", "3.10")
    If pythonExe = "" Then
        On Error Resume Next
        Dim proc, output
        Set proc = shell.Exec("py -" & version & " -c ""import sys; print(sys.executable)""")
        If Err.Number = 0 Then
            Do While proc.Status = 0
                WScript.Sleep 50
            Loop
            output = Trim(proc.StdOut.ReadAll)
            If fso.FileExists(output) Then
                pythonExe = output
            End If
        End If
        Err.Clear
        On Error GoTo 0
    End If
Next

' Fallback to standard installation locations, still restricted to 3.10-3.12.
If pythonExe = "" Then
    For Each version In Array("312", "311", "310")
        If fso.FileExists("C:\Program Files\Python" & version & "\python.exe") Then
            pythonExe = "C:\Program Files\Python" & version & "\python.exe"
            Exit For
        End If
        If localAppData <> "%LOCALAPPDATA%" Then
            If fso.FileExists(localAppData & "\Programs\Python\Python" & version & "\python.exe") Then
                pythonExe = localAppData & "\Programs\Python\Python" & version & "\python.exe"
                Exit For
            End If
        End If
    Next
End If

If pythonExe <> "" Then
    pythonw = fso.BuildPath(fso.GetParentFolderName(pythonExe), "pythonw.exe")
    If Not fso.FileExists(pythonw) Then pythonw = pythonExe
End If

If pythonw = "" Then
    MsgBox "Serenum requires Python 3.10, 3.11 or 3.12. Install Python 3.12 (recommended) and run this shortcut again. Python 3.14 can remain installed.", vbExclamation, "Serenum setup"
    WScript.Quit 3
End If

shell.CurrentDirectory = baseDir
shell.Run Chr(34) & pythonw & Chr(34) & " -X utf8 " & Chr(34) & targetFile & Chr(34), 0, False
