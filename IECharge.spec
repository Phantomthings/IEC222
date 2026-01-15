# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Liste des dossiers à inclure
added_files = [
    ('templates', 'templates'),
    ('static', 'static'),
    ('routers', 'routers'),
]

# Hidden imports pour les modules qui ne sont pas détectés automatiquement
hidden_imports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'asyncua',
    'asyncua.client',
    'asyncua.ua',
    'asyncua.common',
    'fastapi',
    'fastapi.responses',
    'starlette',
    'starlette.responses',
    'starlette.staticfiles',
    'jinja2',
    'jinja2.ext',
    'openpyxl',
    'openpyxl.cell',
    'openpyxl.styles',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='IECharge_SCADA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # True pour voir les logs, False pour masquer la console
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Vous pouvez ajouter un fichier .ico ici si vous en avez un
)
