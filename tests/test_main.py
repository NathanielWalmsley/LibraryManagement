import pytest
from library_manager import main

def test_init_establishes_connection():
    test_path = './tests/sqlite.db'
    catalogue = main.LibraryManager(test_path)
    assert catalogue._connection_path == test_path

