@echo off
echo ========================================
echo  Construction de l'executable IECharge
echo ========================================
echo.

REM Vérifie si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Installation de PyInstaller...
pip install pyinstaller

echo.
echo [2/4] Installation des dépendances...
pip install -r requirements.txt

echo.
echo [3/4] Nettoyage des anciens builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

echo.
echo [4/4] Génération de l'exécutable...
pyinstaller IECharge.spec

echo.
if exist "dist\IECharge_SCADA.exe" (
    echo ========================================
    echo  BUILD REUSSI!
    echo ========================================
    echo.
    echo L'exécutable se trouve dans: dist\IECharge_SCADA.exe
    echo.
    echo Vous pouvez maintenant copier ce fichier n'importe où
    echo et l'exécuter sans avoir besoin d'installer Python.
    echo.
) else (
    echo ========================================
    echo  ERREUR: Le build a échoué
    echo ========================================
    echo Vérifiez les messages d'erreur ci-dessus
    echo.
)

pause
