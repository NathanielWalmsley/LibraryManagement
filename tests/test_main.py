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
    # This test also works for creating a duplicate branch - a new one
    # will not be created
    with pytest.raises(sqlite3.Error):
        CATALOGUE.insert_new_library('Sacramento', 'ABC Fraudulent Blvd, Ohio')


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


def test_get_stock_information_for_multiple_libraries():
    title = 'Dune'
    result = CATALOGUE.get_stock_information(bookTitle=title)
    print(CATALOGUE._execute("""
        SELECT 
                book_loans_BookID as bookId,
                book_loans_BranchID as branchId,
                count(*) as loaned
                FROM tbl_book_loans
                GROUP BY 1, 2
    """))
    assert result == [
        (title, 'Sharpstown', 4),
        (title, 'Central', 5),
        (title, 'Saline', 4),
        (title, 'Ann Arbor', 3)
    ]


def test_get_stock_information_for_a_library():
    title = 'The Hitchhikers Guide to the Galaxy'
    result = CATALOGUE.get_stock_information(title, branchName='Central')
    assert result == [(title, 'Central', 4)]


# ------------------------------- INSERT/UPDATE --------------------------------------- #


# def test_insert_book_or_update_stock_updates_stock_only_for_existing_book():
#     title = 'The Name of the Wind'
#     branch = 'Sharpstown'
#     result = CATALOGUE.insert_book_or_update_stock(
#         title, 
#         'DAW Books', 
#         'Patrick Rothfuss', 
#         branch, 
#         4
#     )
#     result = CATALOGUE.get_stock_information(title, branch)
#     assert result == [(title, branch, 9)]

# def test_insert_book_or_update_stock_add_new_inventory():
#     title = 'Paul Takes the Form of a Mortal Girl'
#     branch = 'Ann Arbor'
#     result = CATALOGUE.insert_book_or_update_stock(
#         title, 
#         'Rescue Press', 
#         'Andrea Lawlor', 
#         branch, 
#         25
#     )
#     result = CATALOGUE.get_stock_information(title, branch)
#     assert result == [(title, branch, 25)]

#     new_author_query = """
#         SELECT * FROM tbl_book_authors 
#         WHERE 
#             book_authors_BookID = 22
#             AND 
#             book_authors_AuthorName = "Andrea Lawlor";
#     """
#     result = CATALOGUE._execute(new_author_query)
#     assert result == [(22, 'Andrea Lawlor', 22)]
