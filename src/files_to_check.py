# src/files_to_check.py
from pathlib import Path

# список файлов
FILES = [
    Path("data/financial_data.csv"),
    Path("data/prolongations.csv"),
]

ID_COL = "id"
ENCODINGS = ["utf-8-sig", "utf-8", "cp1251"]  # типы кодировок
HEAD_ROWS = 5  # количество выводимых строк

