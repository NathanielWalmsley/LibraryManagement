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
    assert 6 not in result # Ensure we didn't add a new entry for the second Sacramento


def test_insert_new_library_returns_false_when_cannot_create_new_branch():
    # Using bad arguments here to create an error with the parameterisation
    assert not CATALOGUE.insert_new_library(
        ['Sacramento', '123 Fake Street, Springfield'], 123
    )


def test_get_books_by_title_filter_by_author():
    result = CATALOGUE.get_books_by_title(author='Patrick Rothfuss')
    assert result == [
        (1, 'The Name of the Wind', 'DAW Books'), 
        (7, 'The Wise Mans Fear', 'DAW Books')
    ]


def test_get_books_by_title_filter_by_publisher():
    result = CATALOGUE.get_books_by_title(publisher='Scholastic')
    assert result == [(15, 'Holes', 'Scholastic')]
    result = CATALOGUE.get_books_by_title(publisher='Bloomsbury')
    assert result == [
        (8, 'Harry Potter and the Philosophers Stone', 'Bloomsbury'), 
        (16, 'Harry Potter and the Chamber of Secrets', 'Bloomsbury'), 
        (17, 'Harry Potter and the Prisoner of Azkaban', 'Bloomsbury')
    ]


def test_get_books_taken_out_by_borrower():
    result = CATALOGUE.get_books_by_title(borrower_id=1)
    assert result == [
        (1, 'The Name of the Wind', 'DAW Books'), 
        (2, 'It', 'Viking'), 
        (3, 'The Green Mile', 'Signet Books'), 
        (4, 'Dune', 'Chilton Books'), 
        (19, 'A Game of Thrones', 'Bantam')
    ]


def test_get_publisher_information_by_address():
    result = CATALOGUE.get_publisher_information(
        address='375 Hudson Street, New York, NY 10014'
    )
    assert result == [
        ('DAW Books', '375 Hudson Street, New York, NY 10014', '212-366-2000'),
        ('Viking', '375 Hudson Street, New York, NY 10014', '212-366-2000'),
        ('Signet Books', '375 Hudson Street, New York, NY 10014', '212-366-2000'),
        ('Chalto & Windus','375 Hudson Street, New York, NY 10014', '212-366-2000'),
        ('Bantam', '375 Hudson Street, New York, NY 10014', '212-366-2000')
    ]


def test_get_borrower_in_possession_of_book():
    result = CATALOGUE.get_borrower_information(book='Dune')
    assert result == [
        (1, 'Joe Smith', '1321 4th Street, New York, NY 10014','212-312-1234'),
        (3, 'Tom Li','981 Main Street, Ann Arbor, MI 48104','734-902-7455')
    ]


# ------------------------------- INSERT/UPDATE --------------------------------------- #


def test_insert_new_book():
    result = CATALOGUE.insert_book_or_update_stock(
        'The Name of the Wind', 
        'DAW Books', 
        'Patrick Rothfuss', 
        'Sharpstown', 
        4
    )
    updated_stock_query = """
        SELECT book_copies_No_Of_Copies 
        FROM tbl_book_copies 
        WHERE book_copies_BranchID = 1 AND book_copies_BookID = 1;
    """
    result = CATALOGUE._execute(updated_stock_query)
    assert result == [(9,)]

    # Check that no other values were updated
    unmodified_stock_query = """
        SELECT book_copies_No_Of_Copies 
        FROM tbl_book_copies 
        WHERE book_copies_BranchID = 1 AND book_copies_BookID = 2;
    """
    result = CATALOGUE._execute(unmodified_stock_query)
    assert result == [(5,)]

