# Guide de Création de l'Exécutable IECharge SCADA

Ce guide explique comment créer un fichier `.exe` standalone de l'application IECharge SCADA qui peut être exécuté n'importe où sans installation de Python.

## 📋 Prérequis

- **Python 3.8+** installé sur votre système
- **Windows** (pour créer un .exe Windows) ou **Linux/Mac** (pour créer un binaire)
- Connexion Internet (pour télécharger les dépendances)

## 🚀 Méthode Rapide (Recommandée)

### Sur Windows

1. Ouvrez l'explorateur de fichiers et naviguez vers le dossier du projet
2. Double-cliquez sur `build_exe.bat`
3. Attendez la fin du processus (quelques minutes)
4. Votre exécutable sera dans le dossier `dist/IECharge_SCADA.exe`

### Sur Linux/Mac

1. Ouvrez un terminal dans le dossier du projet
2. Exécutez : `./build_exe.sh`
3. Attendez la fin du processus
4. Votre exécutable sera dans le dossier `dist/IECharge_SCADA`

## 🔧 Méthode Manuelle

Si vous préférez construire manuellement l'exécutable :

### 1. Installer PyInstaller

```bash
pip install pyinstaller
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Construire l'exécutable

```bash
pyinstaller IECharge.spec
```

### 4. Récupérer l'exécutable

L'exécutable se trouve dans : `dist/IECharge_SCADA.exe` (Windows) ou `dist/IECharge_SCADA` (Linux/Mac)

## 📦 Contenu du Package

L'exécutable généré contient :

- ✅ L'application Python complète
- ✅ Toutes les dépendances (FastAPI, asyncua, etc.)
- ✅ Les templates HTML
- ✅ Les fichiers statiques (CSS, JS, SVG, images)
- ✅ Les modules de routage
- ✅ L'interpréteur Python embarqué

## 🎯 Utilisation de l'Exécutable

Une fois l'exécutable créé :

1. **Copiez** `IECharge_SCADA.exe` où vous voulez
2. **Double-cliquez** sur le fichier pour lancer l'application
3. Une fenêtre console s'ouvrira avec les logs
4. **Ouvrez votre navigateur** à l'adresse : `http://localhost:8000`

### Arguments de Ligne de Commande

Vous pouvez aussi lancer l'application avec des paramètres :

```bash
IECharge_SCADA.exe --host 0.0.0.0 --port 8080
```

Cela permettra d'accéder à l'application depuis d'autres machines sur le réseau.

## ⚙️ Configuration

### Modifier le Port par Défaut

Éditez `main.py` avant de construire l'exécutable :

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)  # Changez 8080
```

### Configuration OPC UA

Le serveur OPC UA est configuré dans `config.py` :

```python
OPCUA_SERVER_URL = "opc.tcp://192.168.10.70:4840"
```

Modifiez cette URL avant de construire l'exécutable si nécessaire.

### Masquer la Console Windows

Si vous voulez que l'exécutable ne montre pas de fenêtre console, éditez `IECharge.spec` :

```python
exe = EXE(
    ...
    console=False,  # Changez True en False
    ...
)
```

Puis reconstruisez l'exécutable.

## 🐛 Dépannage

### L'exécutable ne démarre pas

- **Vérifiez l'antivirus** : Certains antivirus bloquent les exécutables PyInstaller
- **Lancez depuis un terminal** pour voir les messages d'erreur
- **Vérifiez les logs** dans la console

### Erreur "Failed to connect to OPC UA server"

- Vérifiez que le serveur OPC UA (`192.168.10.70:4840`) est accessible
- Vérifiez la configuration réseau
- L'application fonctionnera quand même, mais sans données temps réel

### L'exécutable est trop gros

L'exécutable peut faire 50-100 MB car il contient Python et toutes les dépendances. C'est normal pour un exécutable standalone.

Pour réduire la taille :
- Utilisez UPX (déjà activé dans le .spec)
- Excluez les modules inutilisés

### Temps de démarrage lent

Le premier démarrage peut prendre 10-20 secondes car PyInstaller décompresse les fichiers dans un dossier temporaire.

## 📝 Structure des Fichiers

```
IEC222/
├── build_exe.bat              # Script de build Windows
├── build_exe.sh               # Script de build Linux/Mac
├── IECharge.spec              # Configuration PyInstaller
├── requirements.txt           # Dépendances Python
├── BUILD_EXE_README.md        # Ce fichier
├── main.py                    # Point d'entrée
├── config.py                  # Configuration
├── opcua_client.py            # Client OPC UA
├── routers/                   # Routes API
├── templates/                 # Templates HTML
└── static/                    # Fichiers statiques

Après le build :
├── build/                     # Fichiers temporaires (peut être supprimé)
└── dist/                      # Dossier contenant l'exécutable
    └── IECharge_SCADA.exe     # VOTRE EXÉCUTABLE !
```

## 🔒 Distribution

L'exécutable peut être distribué de plusieurs façons :

1. **Copie directe** : Copiez simplement le fichier .exe
2. **Clé USB** : Mettez-le sur une clé USB pour l'exécuter sur d'autres machines
3. **Réseau** : Partagez-le via un dossier réseau
4. **Archive** : Créez un fichier ZIP contenant l'exécutable

⚠️ **Note** : L'exécutable est spécifique à la plateforme :
- Un .exe Windows ne fonctionnera que sur Windows
- Un binaire Linux ne fonctionnera que sur Linux
- Vous devez construire sur chaque plateforme cible

## 🎉 Félicitations !

Vous avez maintenant un exécutable standalone de votre application SCADA IECharge !

Pour toute question ou problème, consultez la documentation de [PyInstaller](https://pyinstaller.org/).

---

**Version** : 2.0
**Date** : Janvier 2026
**Auteur** : IECharge SCADA Team
