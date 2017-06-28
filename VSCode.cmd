@echo off
set APPS=%USERPROFILE%\Apps
set PATH=%APPS%\IDEs\VSCode;%APPS%\node\7.10.0;%APPS%\WinPython\3.6.1.0Qt5\python-3.6.1.amd64;%PATH%
cd %1
start Code .