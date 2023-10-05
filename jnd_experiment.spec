# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['jnd_experiment.py'],
    pathex=[],
    binaries=[],
    datas=[('audio/', 'audio/'), ('pics/', 'pics/'), ('C:\\Users\\NOLA\\.conda\\envs\\exp_jnd\\Lib\\site-packages\\psychopy\\alerts', 'psychopy/alerts/alertsCatalogue'), ('C:\\Users\\NOLA\\.conda\\envs\\exp_jnd\\Lib\\site-packages\\freetype\\freetype.dll', '.')],
    hiddenimports=['psychopy.visual.backends.pygletbackend', 'psychopy.visual.line'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='jnd_experiment',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=['vcruntime140.dll'],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='C:\\Users\\NOLA\\OneDrive\\PhD\\events_conferences_presentations\\icons\\matroschka_1.ico',
)
