import os
import logging
from collections import namedtuple

# Конфигурация логирования
logging.basicConfig(
    filename="file_info.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Определяем namedtuple для хранения информации о файле или каталоге
FileInfo = namedtuple('FileInfo', ['name', 'extension', 'is_directory', 'parent_directory'])

def collect_file_info(directory_path):
    for entry in os.scandir(directory_path):
        # Получаем информацию о файле или каталоге
        if entry.is_file():
            name, extension = os.path.splitext(entry.name)
            file_info = FileInfo(name=name, extension=extension, is_directory=False, parent_directory=directory_path)
        elif entry.is_dir():
            file_info = FileInfo(name=entry.name, extension="", is_directory=True, parent_directory=directory_path)
        else:
            continue

        # Логируем информацию
        logging.info(file_info)

        # Рекурсивно обрабатываем подкаталоги
        if file_info.is_directory:
            collect_file_info(entry.path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py DIRECTORY_PATH")
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    # Преобразуем путь в формат, подходящий для macOS
    directory_path = os.path.abspath(directory_path)

    collect_file_info(directory_path)
