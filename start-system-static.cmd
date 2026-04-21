@echo off
setlocal
powershell -ExecutionPolicy Bypass -File "%~dp0start-system-static.ps1" %*
endlocal