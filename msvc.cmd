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
python setup.py build_ext -b ../.. -t ./ztmp
goto :end

:html
cython -a -o ztmp\%module%.c %module%.pyx
goto :end

:clean
echo Cleaning
rmdir /s /q ztmp\Release
del /q ztmp\*.*
del %module%.c
goto :end

:clean_all
echo Cleaning all
rmdir /s /q ztmp\Release
del /q ztmp\*.*
del %module%.c
del %module%*.pyd
goto :end

:end
if defined err echo %err%
echo FIN

endlocal