:: ACCIONES DE COMPILACIÓN DE _cx.pyd
@echo off
setlocal

if not defined PYTHON_ROOT goto :err_python_root

set module=_zx

if not "%~1"=="" goto :%~1
goto :build

:err_python_root
set err=ERROR: PYTHON_ROOT NO DEFINIDA
goto :end

:build
echo Building %module%.pyd
cython -a -o ztmp\%module%.c %module%.pyx
gcc -c -DMS_WIN64 -Ofast -I%PYTHON_ROOT%\include -o ztmp\%module%.o ztmp\%module%.c
gcc -shared -L%PYTHON_ROOT%\libs -o %module%.pyd ztmp\%module%.o -lpython35
goto :end

:clean
echo Cleaning
del /q ztmp\*.*
goto :end

:clean_all
echo Cleaning all
del %module%*.pyd
del /q ztmp\*.*
goto :end

:end
if defined err echo %err%
echo FIN

endlocal