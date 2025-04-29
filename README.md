# Flashcard App

Simple flashcard app built with Python and Tkinter.

## Features
- Create and study flashcards
- Easy-to-use interface
- Custom icon support for macOS apps

## How to run

```bash
python flashcard.py
HOW TO BUILD macOS .APP
pip install pyinstaller 
Build the app:
pyinstaller --clean --windowed --name flashcard --icon=MyIcon.icns flashcard.py
If you have icon display problems on macOS, you may need the sign the app
codesign --force --deep --sign - path/to/flashcard.app
