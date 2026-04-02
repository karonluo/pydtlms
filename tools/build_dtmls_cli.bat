@echo off
setlocal

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set PYTHON_EXE=%PROJECT_ROOT%\.venv\Scripts\python.exe
set DIST_DIR=%SCRIPT_DIR%dist
set BUILD_DIR=%SCRIPT_DIR%build
set DIST_EXE=%DIST_DIR%\dtmls_cli.exe
set DIST_INI=%DIST_DIR%\dtmls_cli.ini

if not exist "%PYTHON_EXE%" (
  echo 未找到 Python 解释器: %PYTHON_EXE%
  exit /b 1
)

"%PYTHON_EXE%" -m PyInstaller --noconfirm --clean --onefile --name dtmls_cli --distpath "%DIST_DIR%" --workpath "%BUILD_DIR%" "%SCRIPT_DIR%dtmls_cli.py"
if errorlevel 1 exit /b 1

copy /Y "%SCRIPT_DIR%dtmls_cli.ini" "%DIST_INI%" >nul
echo 已生成: %DIST_EXE%
echo 已复制配置: %DIST_INI%

endlocal