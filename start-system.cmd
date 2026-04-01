@echo off
setlocal
powershell -ExecutionPolicy Bypass -File "%~dp0start-system.ps1" %*
endlocal
