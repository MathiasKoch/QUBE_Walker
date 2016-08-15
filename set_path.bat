:: PATH-ADD - add a path to user path environment variable

@echo off
setlocal

:: set user path
set ok=0
for /f "skip=2 tokens=3*" %%a in ('reg query HKCU\Environment /v PATH') do if [%%b]==[] ( setx PATH "%%~a;%programfiles(x86)%\Graphviz2.38\bin" && set ok=1 ) else ( setx PATH "%%~a %%~b;%programfiles(x86)%\Graphviz2.38\bin" && set ok=1 )
if "%ok%" == "0" setx PATH "%programfiles(x86)%\Graphviz2.38\bin"

:end
endlocal
echo.
pause