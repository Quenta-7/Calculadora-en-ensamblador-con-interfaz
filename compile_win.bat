@echo off
:: ============================================
:: compile_win.bat
:: Genera libcalc.dll para Windows
:: Requiere: NASM para Windows + Visual Studio
:: ============================================

echo.
echo Compilando modulos para interfaz Python (Windows)...
echo.

:: Crear carpeta build si no existe
if not exist build mkdir build

:: ── Buscar vcvars64.bat de Visual Studio ──────────────────
set VCVARS=""
for /f "delims=" %%i in ('"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath 2^>nul') do set VS_PATH=%%i
if defined VS_PATH set VCVARS="%VS_PATH%\VC\Auxiliary\Build\vcvars64.bat"

if %VCVARS%=="" (
    echo ERROR: No se encontro Visual Studio.
    echo Instala Visual Studio con "Desarrollo de escritorio con C++"
    pause
    exit /b 1
)

:: Activar entorno MSVC
call %VCVARS% >nul 2>&1
echo Entorno MSVC activado.
echo.

:: ── Verificar NASM ────────────────────────────────────────
where nasm >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: NASM no encontrado en PATH.
    echo Descarga e instala desde: https://www.nasm.us
    echo Asegurate de agregar NASM al PATH durante la instalacion.
    pause
    exit /b 1
)

:: ── Compilar modulos ASM ──────────────────────────────────
echo Compilando aritmetica.asm  (Jose^)...
nasm -f win64 src\aritmetica.asm -o build\aritmetica.obj
if %errorlevel% neq 0 ( echo ERROR en aritmetica.asm & pause & exit /b 1 )

echo Compilando logica.asm      (Efrain^)...
nasm -f win64 src\logica.asm -o build\logica.obj
if %errorlevel% neq 0 ( echo ERROR en logica.asm & pause & exit /b 1 )

echo Compilando conversion.asm  (Emmi^)...
nasm -f win64 src\conversion.asm -o build\conversion.obj
if %errorlevel% neq 0 ( echo ERROR en conversion.asm & pause & exit /b 1 )

:: ── Enlazar DLL ───────────────────────────────────────────
echo.
echo Enlazando libcalc.dll...
link /DLL /NOENTRY /NODEFAULTLIB ^
     /DEF:src\libcalc.def ^
     /OUT:build\libcalc.dll ^
     build\aritmetica.obj ^
     build\logica.obj ^
     build\conversion.obj

if %errorlevel% neq 0 ( echo ERROR al generar libcalc.dll & pause & exit /b 1 )

echo.
echo libcalc.dll generada exitosamente!
echo.
echo Archivos generados:
dir build\libcalc.dll
echo.
echo Ejecutar interfaz: python calculadora_gui.py
pause