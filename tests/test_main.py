import pytest
import sqlite3
from library_manager import main


TEST_PATH = ':memory:'
CATALOGUE = main.LibraryManager(TEST_PATH)
with open('./tests/test_schema.sql', 'r') as fp:
    CATALOGUE.connection.cursor().executescript(fp.read())


def test_init_establishes_connection():
    assert CATALOGUE._connection_path == TEST_PATH


def test_retrieve_list_of_libraries():
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


def test_insert_new_library_returns_true_when_new_branch_created():
    assert CATALOGUE.insert_new_library('Sacramento', '123 Fake Street, Springfield')


def test_insert_new_library_does_not_overwrite_existing_entries():
    CATALOGUE.insert_new_library('Sacramento', '123 Fake Street, Springfield')
    CATALOGUE.insert_new_library('Sacramento', 'ABC Fraudulent Blvd, Ohio')
    result = CATALOGUE.get_all_libraries()
    expected = {
        'library_branch_BranchName': 'Sacramento',
        'library_branch_BranchAddress': '123 Fake Street, Springfield'
    }
    assert result[5] == expected
    assert 6 not in result


def test_insert_new_library_returns_false_when_cannot_create_new_branch():
    # Using bad arguments here to create an error with the parameterisation
    assert not CATALOGUE.insert_new_library(
        ['Sacramento', '123 Fake Street, Springfield'], 123
    )


def test_get_books_by_title_filter_by_author():
    expected = 'The Name of the Wind'
    CATALOGUE.connection.cursor().execute('''INSERT INTO tbl_book
		(book_Title, book_PublisherName)
		VALUES 
		(?, 'DAW Books'), ('The Lorax', 'Harper and Row');''', [expected])
    CATALOGUE.connection.cursor().execute('''
    INSERT INTO tbl_book_authors
		(book_authors_BookID,book_authors_AuthorName)
		VALUES
		('1','Patrick Rothfuss'),
        ('2', 'Dr. Seuss');
    ''')
    result = CATALOGUE.get_books_by_title(author='Patrick Rothfuss')
    assert result == [(expected,)]
    