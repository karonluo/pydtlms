Option Explicit

Dim fso
Set fso = CreateObject("Scripting.FileSystemObject")

Dim logPath
logPath = fso.BuildPath(fso.GetParentFolderName(WScript.ScriptFullName), "powerdesigner_validate_model.log")

Sub WriteLog(message)
   Dim stream
   Set stream = fso.OpenTextFile(logPath, 8, True)
   stream.WriteLine message
   stream.Close
End Sub

If fso.FileExists(logPath) Then
   fso.DeleteFile logPath, True
End If

If WScript.Arguments.Count = 0 Then
   WriteLog "ERROR: missing model path argument"
   WScript.Quit 2
End If

Dim modelPath
modelPath = WScript.Arguments(0)

On Error Resume Next
Dim openedModel
Set openedModel = OpenModel(modelPath, omf_DontOpenView Or omf_Hidden)
If Err.Number <> 0 Then
   WriteLog "ERROR: OpenModel failed: " & Err.Description
   WScript.Quit 3
End If
On Error GoTo 0

If openedModel Is Nothing Then
   WriteLog "ERROR: model is Nothing"
   WScript.Quit 4
End If

WriteLog "OPEN_OK"
WriteLog "NAME=" & openedModel.Name
WriteLog "CODE=" & openedModel.Code
WriteLog "CLASS=" & openedModel.ClassName

On Error Resume Next
WriteLog "TABLES=" & openedModel.Tables.Count
If Err.Number <> 0 Then
   WriteLog "TABLES=ERR:" & Err.Description
   Err.Clear
End If

WriteLog "REFERENCES=" & openedModel.References.Count
If Err.Number <> 0 Then
   WriteLog "REFERENCES=ERR:" & Err.Description
   Err.Clear
End If

WriteLog "DIAGRAMS=" & openedModel.PhysicalDiagrams.Count
If Err.Number <> 0 Then
   WriteLog "DIAGRAMS=ERR:" & Err.Description
   Err.Clear
End If
On Error GoTo 0

openedModel.Close
WScript.Quit 0