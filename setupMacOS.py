import os
from setuptools import setup

APP = ['RandEmailAlias.py']
DATA_FILES = [os.path.join(os.path.abspath('.'), 'REAG-BG.jpg'), os.path.join(os.path.abspath('.'), 'REAM_icon.icns')]
OPTIONS = {
    'packages': ['random', 'string', 'smtplib', 'ssl', 'tkinter', 'pyperclip', 'threading'],
    'iconfile': 'REAM_icon.icns',
    'plist': {
        'CFBundleName': 'RandEmailAlias',
        'CFBundleShortVersionString': '2.4-beta',
        'CFBundleVersion': '2.4-beta',
        'CFBundleExecutable': 'RandEmailAlias',
        'LSUIElement': '1',
    }
}

setup(
    app=APP,
    name='RandEmailAlias',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
