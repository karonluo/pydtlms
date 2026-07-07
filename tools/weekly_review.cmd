@echo off
setlocal
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
chcp 65001 > nul
"C:\Python314\python.exe" "D:\pyproj\pydtlms\tools\weekly_review.py" --days 7 --save >> "D:\pyproj\pydtlms\documents\周报\weekly_review.log" 2>&1
endlocal