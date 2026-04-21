@echo off
setlocal
powershell -ExecutionPolicy Bypass -File "%~dp0start-system-preview.ps1" %*
endlocal
