import pytest
import sqlite3
from library_manager import main


TEST_PATH = './tests/sqlite.db'


def test_init_establishes_connection():
    catalogue = main.LibraryManager(TEST_PATH)
    assert catalogue._connection_path == TEST_PATH


def test_retrieve_list_of_libraries():
    catalogue = main.LibraryManager(TEST_PATH)
    catalogue.connection.cursor().execute("""
    INSERT INTO tbl_library_branch
		(library_branch_BranchName, library_branch_BranchAddress)
		VALUES
		('Sharpstown','32 Corner Road, New York, NY 10012'),
		('Central','491 3rd Street, New York, NY 10014'),
		('Saline','40 State Street, Saline, MI 48176'),
		('Ann Arbor','101 South University, Ann Arbor, MI 48104');
    """)
    result = catalogue.get_all_libraries()
    expected = {
        1: {
            'library_branch_BranchName': 'Sharpstown', 
            'library_branch_BranchAddress': '32 Corner Road, New York, NY 10012'
        },
        2: {
            'library_branch_BranchName': 'Central', 
            'library_branch_BranchAddress': '491 3rd Street, New York, NY 10014'
        },
        3: {
            'library_branch_BranchName': 'Saline', 
            'library_branch_BranchAddress': '40 State Street, Saline, MI 48176'
        },
		4: {
            'library_branch_BranchName': 'Ann Arbor',
            'library_branch_BranchAddress': '101 South University, Ann Arbor, MI 48104'
        }
    }
    assert result == expected

def test_get_none_if_data_doesnt_exist():
    catalogue = main.LibraryManager(TEST_PATH)
    assert catalogue.get_all_libraries() == None
