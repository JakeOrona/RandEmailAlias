from setuptools import setup

APP = ['RandEmailAlias_v2.py']
DATA_FILES = []
OPTIONS = {
    'packages': ['random', 'string', 'smtplib', 'ssl', 'tkinter', 'pyperclip', 'threading'],
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'RandEmailAlias',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
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
