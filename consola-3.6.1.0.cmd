@echo off
color 1E
set APPS=%USERPROFILE%\Apps
set PYTRT=%APPS%\WinPython\3.6.1.0Qt5\python-3.6.1.amd64
set MGWRT=%APPS%\mingw64-6.3.0
set SCIRT=%APPS%\IDEs\wscite
set CODRT=%APPS%\IDEs\VSCode

set PATH=%PYTRT%;%PYTRT%\Scripts;%MGWRT%\bin;%SCIRT%;%CODRT%;%PATH%
set PROMPT=CONSOLA 3.6.1 - $P$_$G
cmd
