Option Explicit

Const ForWriting = 2

Dim system
Set system = CreateObject("Scripting.FileSystemObject")

Dim logPath
logPath = "D:\pyproj\pydtlms\tools\powerdesigner_create_sample_pdm.log"

Sub WriteLog(message)
   Dim file
   Set file = system.OpenTextFile(logPath, ForWriting, True)
   file.WriteLine message
   file.Close
End Sub

Dim outputPath
outputPath = "D:\pyproj\pydtlms\documents\pd_minimal_sample.pdm"

On Error Resume Next
Dim pdm
Set pdm = CreateModel(PdPDM.cls_Model, "|DBMS=Sybase AS Anywhere 9")
If Err.Number <> 0 Then
   WriteLog "CREATE_ERR: " & Err.Description
   Exit Sub
End If

pdm.Name = "copilot_sample"
pdm.Code = "copilot_sample"
pdm.SaveAs outputPath
If Err.Number <> 0 Then
   WriteLog "SAVE_ERR: " & Err.Description
   Exit Sub
End If

WriteLog "CREATE_OK"
WriteLog outputPath

pdm.Close