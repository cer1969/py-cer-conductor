@echo off
COLOR 1E

set PYVER=35 
set APPS=%USERPROFILE%\Apps
set PYTRT=%APPS%\WinPython\3.5.3.1Zero\python-3.5.3.amd64
set MGWRT=%APPS%\mingw64-6.3.0
set SCIRT=%APPS%\IDEs\wscite
set CODRT=%APPS%\IDEs\VSCode
set NODRT=%APPS%\node\7.10.0

set PATH=%PYTRT%;%PYTRT%\Scripts;%MGWRT%\bin;%SCIRT%;%CODRT%;%NODRT%;%PATH%
set PROMPT=CONSOLA 3.5.3 - $P$_$G
cmd