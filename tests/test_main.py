import pytest
import sqlite3
from library_manager import main


TEST_PATH = './tests/sqlite.db'
CATALOGUE = main.LibraryManager(TEST_PATH)


def test_init_establishes_connection():
    assert CATALOGUE._connection_path == TEST_PATH


def test_retrieve_list_of_libraries():
    CATALOGUE.connection.cursor().execute("""
    INSERT INTO tbl_library_branch
		(library_branch_BranchName, library_branch_BranchAddress)
		VALUES
		('Sharpstown','32 Corner Road, New York, NY 10012'),
		('Central','491 3rd Street, New York, NY 10014'),
		('Saline','40 State Street, Saline, MI 48176'),
		('Ann Arbor','101 South University, Ann Arbor, MI 48104');
    """)
    result = CATALOGUE.get_all_libraries()
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
    # Clean up any records created in this test
    CATALOGUE.connection.cursor().execute('DELETE FROM tbl_library_branch')


def test_get_none_if_data_doesnt_exist():
    assert CATALOGUE.get_all_libraries() == None


def test_insert_new_library_returns_true_when_new_branch_created():
    assert CATALOGUE.insert_new_library('Sacramento', '123 Fake Street, Springfield')
    

def test_insert_new_library_returns_false_when_cannot_create_new_branch():
    # Using bad arguments here to create an error with the parameterisation
    assert not CATALOGUE.insert_new_library(['Sacramento', '123 Fake Street, Springfield'], 123)