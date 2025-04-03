# update_translations.py
import os
import subprocess

def update_translations():
    # Список языков
    languages = ['ru', 'fr', 'de', 'es']
    
    # Список файлов с переводимыми строками
    sources = ['app/main_window.py', 'app/infoDialog.py']
    
    # Создаем .ts файлы
    for lang in languages:
        cmd = f"pylupdate6 --verbose {' '.join(sources)} -ts translations/photoarchive_{lang}.ts"
        subprocess.run(cmd, shell=True)
    
    print("Translation files created. Now you can edit them with Qt Linguist.")

def compile_translations():
    languages = 'ru '#['ru', 'fr', 'de', 'es']
    for lang in languages:
        cmd = f"lrelease translations/photoarchive_{lang}.ts"
        subprocess.run(cmd, shell=True)
    
    print("Translations compiled to .qm files.")

if __name__ == '__main__':
    update_translations()
    # После редактирования файлов в Qt Linguist, раскомментируйте следующую строку:
    compile_translations()