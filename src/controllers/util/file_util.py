from pathlib import Path
from uuid import UUID
from fastapi import File
from collections import Counter

from src.config.settings import get_settings

def get_root() -> Path:
    """Get Root of Project"""
    return Path(__file__).parent.parent.parent

def get_file_folder() -> Path:
    """Get Path of Folder for textfiles """
    return Path(get_root(), get_settings().upload_folder)

def gen_file(uuid: UUID, file: File) -> Path:
    """ generate Path for """
    filename = f"{uuid}_____{file.filename}"
    return Path(get_file_folder(), filename)

def most_frequent_char(string):
    d = Counter(string.replace(' ', '').lower())
    return d.most_common()[0]

def reverse_string(x):
  return x[::-1]