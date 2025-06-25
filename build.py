import PyInstaller.__main__
import shutil
import os

# Очистка предыдущих сборок
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

# Параметры сборки
PyInstaller.__main__.run([
    'app.py',               # Основной файл приложения
    '--onefile',            # Создать один EXE-файл
    '--windowed',           # Для GUI-приложений (без консоли)
    '--icon=app.ico',       # Иконка приложения (необязательно)
    '--name=SentimentAnalyzer',  # Имя выходного файла
    '--add-data=src;src',   # Добавление папки с моделями
    '--hidden-import=transformers.models.bert',  # Важные скрытые импорты
    '--hidden-import=torch',
    '--hidden-import=tkinter',
    '--clean'               # Очистка временных файлов
])

# НЕ РАБОТАЕТ