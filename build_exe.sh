#!/bin/bash

echo "========================================"
echo " Construction de l'executable IECharge"
echo "========================================"
echo ""

# Vérifie si Python est installé
if ! command -v python3 &> /dev/null
then
    echo "ERREUR: Python3 n'est pas installé"
    echo "Veuillez installer Python3"
    exit 1
fi

echo "[1/4] Installation de PyInstaller..."
pip3 install pyinstaller

echo ""
echo "[2/4] Installation des dépendances..."
pip3 install -r requirements.txt

echo ""
echo "[3/4] Nettoyage des anciens builds..."
rm -rf build dist

echo ""
echo "[4/4] Génération de l'exécutable..."
pyinstaller IECharge.spec

echo ""
if [ -f "dist/IECharge_SCADA" ]; then
    echo "========================================"
    echo " BUILD REUSSI!"
    echo "========================================"
    echo ""
    echo "L'exécutable se trouve dans: dist/IECharge_SCADA"
    echo ""
    echo "Vous pouvez maintenant copier ce fichier n'importe où"
    echo "et l'exécuter sans avoir besoin d'installer Python."
    echo ""
else
    echo "========================================"
    echo " ERREUR: Le build a échoué"
    echo "========================================"
    echo "Vérifiez les messages d'erreur ci-dessus"
    echo ""
fi
