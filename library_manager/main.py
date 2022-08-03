from email.mime import base
import sqlite3


class LibraryManager(object):

    def __init__(self, path):
        self._connection_path = path
        self.connection = None
        try:
            self.connection = sqlite3.connect(path)
            print('Connection to SQLite Database established')
        except sqlite3.Error as e:
            print(f'Unable to establish connection to SQLite database at {path}')
            print(f'Error occured with the following message: {e}')

    def _execute(self, query, parameters=[]):
        '''
            Requires:
                query (string)
                parameters (iterable)
        '''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, parameters)
            result = cursor.fetchall()
            cursor.close()
            return result
        except sqlite3.Error as e:
            print(
                f'An SQL Error for the connection to "{self._connection_path}" '
                f'occurred for the query:\n'
                f'{query}\n'
                f'with parameters: {parameters}\n'
                f'Error code is: {e}'
            )
        except Exception as unexpectedException:
            print(
                f'An unexpected error occurred with code: {unexpectedException}'
            )
            raise

    def get_all_libraries(self):
        """
            Get a complete list of all the libraries managed by this
            catalogue and return them as a dictionary
        """
        query = """
            SELECT * FROM tbl_library_branch;
        """
        result_raw = self._execute(query)
        if not result_raw:
            return
        
        result_processed = dict()
        for row in result_raw:
            result_processed.update({
                row[0]: {
                    'library_branch_BranchName': row[1],
                    'library_branch_BranchAddress': row[2]
                    }
                })
        return result_processed

    def _execute_query_with_conditions(self, table, conditions, kwargs):
        query = f'SELECT * FROM {table}'
        parameters = []

        if len(kwargs) > 0:
            query += '\nWHERE'

        for condition, value in kwargs.items():
            if condition in conditions:
                query += conditions[condition]
                parameters.append(value)

        return self._execute(query, parameters)

    def get_books_by_title(self, **kwargs):
        conditions = {
            'title': '\n\tbook_Title = ?',
            'author': '\n\tbook_BookID IN ' +
                '(SELECT book_authors_BookID ' +
                    'FROM tbl_book_authors ' +
                    'WHERE book_authors_AuthorName = ?)',
            'publisher': '\n\tbook_PublisherName = ?',
            'borrower_id': '\n\tbook_BookID IN ' +
                '(SELECT book_loans_BookID FROM tbl_book_loans ' +
                    'WHERE book_loans_CardNo IN ' +
                        '(SELECT borrower_CardNo FROM tbl_borrower WHERE borrower_CardNo = ?))',
        }
        return self._execute_query_with_conditions('tbl_Book', conditions, kwargs)

    def get_publisher_information(self, **kwargs):
        conditions = {
            'name': '\n\tpublisher_PublisherName = ?',
            'address': '\n\tpublisher_PublisherAddress = ?',
            'phone': '\n\tpublisher_PublisherPhone = ?'
        }
        return self._execute_query_with_conditions('tbl_Publisher', conditions, kwargs)
        
    def get_borrower_information(self, **kwargs):
        conditions = {
            'name': '\n\tborrower_BorrowerName = ?',
            'address': '\n\tborrower_BorrowerAddress = ?',
            'phone': '\n\tborrower_BorrowerPhone = ?',
            'book': '\n\tborrower_CardNo IN ' +
                '(SELECT book_loans_CardNo FROM tbl_book_loans ' +
                    'WHERE book_loans_BookID IN ' +
                        '(SELECT book_BookID FROM tbl_book WHERE book_Title = ?))'
        }
        return self._execute_query_with_conditions('tbl_Borrower', conditions, kwargs)

# ---------------------------------INSERT/UPDATE QUERIES--------------------------------#

    def insert_new_library(self, branch_name, branch_address):
        '''
            Create a new library branch to monitor. 
            Requires:
                branch_name (string)
                branch_address (string)
            Returns:
                Boolean - True for successful creation, False for unsuccessful
        '''
        query = """
            INSERT INTO 
                tbl_library_branch (library_branch_BranchName, library_branch_BranchAddress)
            VALUES
                (?, ?);
        """
        result = self._execute(query, parameters=(branch_name, branch_address))
        return result == [] # The result of fetchall() if insert succeeds

    def insert_book_or_update_stock(
                self, title, publisher, author, branch, stock
        ):
        '''
            To create a new book, we need to know: 
            - its title,
            - who wrote it
            - who published it
            - where the stock is kept
            - how many copies we have
            This method deliberately avoids the case of updating book
            information except for stock availability - we will only 
            add new books with unique title-author combinations.
        '''
        # Create the entry in tbl_book - do nothing if the book
        # already exists
        insert_book = """
            INSERT INTO tbl_book(book_Title, book_PublisherName)
            VALUES (?, ?)
            ON CONFLICT (book_Title, book_PublisherName) DO NOTHING;
        """
        self._execute(insert_book, [title, publisher])
        get_book_id = """
            SELECT book_BookID FROM tbl_book WHERE book_Title = ? AND book_PublisherName = ?
        """
        book_id = self._execute(get_book_id, [title, publisher])[0][0]

        # Add or update the stock at the branch
        get_branch_id = """
            SELECT library_branch_BranchID FROM tbl_library_branch WHERE library_branch_BranchName = ?;
        """
        branch_id = self._execute(get_branch_id, [branch])[0][0]
        update_stock = """
            INSERT INTO tbl_book_copies(book_copies_BookID, book_copies_BranchID, book_copies_No_Of_Copies)
            VALUES (?, ?, ?)
            ON CONFLICT (book_copies_BookID, book_copies_BranchID) 
            DO UPDATE SET book_copies_No_Of_Copies = book_copies_No_Of_Copies + ?;
        """
        self._execute(update_stock, [book_id, branch_id, stock, stock])

        # Add the book's author - do nothing if the author already
        # already exists for that book
        add_author = """
            INSERT INTO tbl_book_authors (book_authors_BookID, book_authors_AuthorName)
            VALUES (?, ?)
            ON CONFLICT (book_authors_BookID, book_authors_AuthorName)
            DO NOTHING;
        """
        self._execute(add_author, [book_id, author])