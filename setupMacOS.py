from setuptools import setup

APP = ['RandEmailAlias.py']
DATA_FILES = ["REAG-BG.jpg"]
OPTIONS = {
    'packages': ['random', 'string', 'smtplib', 'ssl', 'tkinter', 'pyperclip', 'threading'],
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'RandEmailAlias',
        'CFBundleShortVersionString': '2.4-beta',
        'CFBundleVersion': '2.4-beta',
        'CFBundleExecutable': 'RandEmailAlias',
        'LSUIElement': '1',
    },
    'resources': ['icon.icns'],
}

setup(
    app=APP,
    name='RandEmailAlias',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
