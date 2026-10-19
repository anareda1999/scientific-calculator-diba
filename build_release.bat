@echo off
REM ============================================================================
REM  DIDA Scientific Calculator - Release Build
REM  Builds the .exe, adds the user guide and packages a ZIP for the client.
REM
REM  Usage:  double-click this file, or run  build_release.bat  in a terminal
REM ============================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ============================================================
echo   DIDA SCIENTIFIC CALCULATOR  -  RELEASE BUILD
echo ============================================================
echo.

REM --- 1/5  tests -------------------------------------------------------------
echo [1/5] Running unit tests...
python tests\test_engine.py
if errorlevel 1 (
    echo.
    echo [!] TESTS FAILED - build aborted.
    pause
    exit /b 1
)
python tests\test_calculus.py
if errorlevel 1 (
    echo.
    echo [!] TESTS FAILED - build aborted.
    pause
    exit /b 1
)
echo.

REM --- 2/5  clean -------------------------------------------------------------
echo [2/5] Cleaning previous build...
taskkill /f /im ScientificCalculator.exe >nul 2>&1
if exist "dist\ScientificCalculator.exe" del /f /q "dist\ScientificCalculator.exe"
if exist "release" rmdir /s /q "release"
echo       done.
echo.

REM --- 3/5  compile -----------------------------------------------------------
echo [3/5] Building the executable with PyInstaller...
pyinstaller ScientificCalculator.spec --noconfirm --log-level WARN
if errorlevel 1 (
    echo.
    echo [!] BUILD FAILED.
    pause
    exit /b 1
)
echo       done.
echo.

REM --- 4/5  package -----------------------------------------------------------
echo [4/5] Packaging the release for the client...
if not exist "release" mkdir "release"
if not exist "release\Calculatrice_Scientifique_DIDA" mkdir "release\Calculatrice_Scientifique_DIDA"

copy /y "dist\ScientificCalculator.exe" "release\Calculatrice_Scientifique_DIDA\" >nul
copy /y "docs\GUIDE_UTILISATION.txt"    "release\Calculatrice_Scientifique_DIDA\" >nul
copy /y "docs\GUIDE_UTILISATION.html"   "release\Calculatrice_Scientifique_DIDA\" >nul
copy /y "README.md"                    "release\Calculatrice_Scientifique_DIDA\" >nul

REM zip the folder (built into Windows 10+)
powershell -NoProfile -Command "Compress-Archive -Path 'release\Calculatrice_Scientifique_DIDA' -DestinationPath 'release\Calculatrice_Scientifique_DIDA_v2.0.zip' -Force" >nul 2>&1

echo       done.
echo.

REM --- 5/5  summary -----------------------------------------------------------
echo [5/5] Release summary
echo ------------------------------------------------------------
if exist "release\Calculatrice_Scientifique_DIDA_v2.0.zip" (
    for %%F in ("release\Calculatrice_Scientifique_DIDA_v2.0.zip") do echo        ZIP  : %%~nxF  (%%~zF bytes)
)
if exist "dist\ScientificCalculator.exe" (
    for %%F in ("dist\ScientificCalculator.exe") do echo        EXE  : %%~nxF  (%%~zF bytes)
)
echo ------------------------------------------------------------
echo.
echo   Give your client the ZIP file:
echo     release\Calculatrice_Scientifique_DIDA_v2.0.zip
echo.
echo   It contains:
echo     - ScientificCalculator.exe  (the program - no installation needed)
echo     - GUIDE_UTILISATION.txt     (how to use, plain text)
echo     - GUIDE_UTILISATION.html    (how to use, colourful - open in browser)
echo     - README.md
echo.
pause
