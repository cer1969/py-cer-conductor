@echo off
COLOR F1
set PYTHON_ROOT=C:\Users\crecheverria\Apps\WinPython\3.6.1.0Zero\python-3.6.1.amd64
set MINGW_ROOT=C:\Users\crecheverria\Apps\mingw
set SCITE_ROOT=C:\Users\crecheverria\Apps\IDEs\wscite
SET CODE_ROOT=C:\Users\crecheverria\Apps\IDEs\VSCode

SET PATH=%PYTHON_ROOT%;%PYTHON_ROOT%\Scripts;%MINGW_ROOT%\bin;%SCITE_ROOT%;%CODE_ROOT%;%PATH%
SET PROMPT=CONSOLA 3.6.1 - $P$_$G
cmd
