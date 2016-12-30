:: ACCIONES DE COMPILACIÓN DE _cx.pyd
@echo off
setlocal

if not defined PYTHON_DEV goto :err_python_dev

set module=_zx

if not "%~1"=="" goto :%~1
goto :build

:err_python_dev
set err=ERROR: PYTHON_DEV NO DEFINIDA
goto :end

:build
echo Building %module%.pyd
cython -a -o ztmp\%module%.c %module%.pyx
gcc -c -DMS_WIN64 -Ofast -I%PYTHON_DEV%\include -o ztmp\%module%.o ztmp\%module%.c
gcc -shared -L%PYTHON_DEV%\libs -o %module%.pyd ztmp\%module%.o -lpython35
goto :end

:clean
echo Cleaning tmp
del ztmp\%module%.c
del ztmp\%module%.o
del ztmp\%module%.html
goto :end

:clean_all
echo Cleaning all
del %module%.pyd
del ztmp\%module%.c
del ztmp\%module%.o
del ztmp\%module%.html
goto :end

:end
if defined err echo %err%
echo FIN

endlocal