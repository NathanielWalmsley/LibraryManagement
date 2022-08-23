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
            raise
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
            SELECT * FROM library_branch;
        """
        result_raw = self._execute(query)
        if not result_raw:
            return
        
        result_processed = dict()
        for row in result_raw:
            result_processed.update({
                row[0]: {
                    'name': row[1],
                    'address': row[2]
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

    def get_book_information(self, **kwargs):
        conditions = {
            'title': '\n\t title = ?',
            'author': '\n\t id IN ' +
                '(SELECT book_id ' +
                    'FROM book_author_link ' +
                    'JOIN author ON author.id = author_id '
                    'WHERE name = ?)',
            'publisher': '\n\t publisher = ?',
            'borrower_id': '\n\t id IN ' +
                '(SELECT book_id FROM loan ' +
                    'WHERE card_number IN ' +
                        '(SELECT card_number FROM borrower WHERE card_number = ?))',
        }
        return self._execute_query_with_conditions('book', conditions, kwargs)

    # def get_publisher_information(self, **kwargs):
    #     conditions = {
    #         'name': '\n\tpublisher_PublisherName = ?',
    #         'address': '\n\tpublisher_PublisherAddress = ?',
    #         'phone': '\n\tpublisher_PublisherPhone = ?'
    #     }
    #     return self._execute_query_with_conditions('tbl_publisher', conditions, kwargs)
        
    def get_borrower_information(self, **kwargs):
        conditions = {
            'name': '\n\tname = ?',
            'address': '\n\taddress = ?',
            'phone': '\n\tphone = ?',
            'book': '\n\tcard_number IN ' +
                '(SELECT card_number FROM loan ' +
                    'WHERE book_id IN ' +
                        '(SELECT id FROM book WHERE title = ?))'
        }
        return self._execute_query_with_conditions('borrower', conditions, kwargs)

    def get_stock_information(self, bookTitle, branchName=None):
        '''
            Retrieve information about a single book in one or more libraries.
            If there are no copies of a book in a library, an empty row will be returned.
            Returns:
            List of tuples represents the rows being returned in the format:
            Title; Branch; Total copies in the branch; Copies on loan
        '''
        query = f"""
            SELECT
                book.title, 
                library_branch.name,
                stock,
                COUNT(loan.id)
            FROM 
                inventory
            LEFT JOIN loan
                ON inventory.book_id = loan.book_id 
                AND inventory.branch_id = loan.branch_id
            JOIN book
                ON inventory.book_id = book.id
            JOIN library_branch
                ON inventory.branch_id = library_branch.id
            WHERE 
                book.title = ?
            {"AND library_branch.name = ?" if branchName else ""}
            GROUP BY inventory.book_id, inventory.branch_id
        """
        if branchName:
            return self._execute(query, [bookTitle, branchName])
        return self._execute(query, [bookTitle])

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
                library_branch (name, address)
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
            INSERT INTO book (title, publisher) VALUES (?, ?)
            ON CONFLICT (title, publisher) DO NOTHING
        """
        self._execute(insert_book, [title, publisher])
        get_book_id = """
            SELECT id FROM book WHERE title = ? AND publisher = ?
        """
        book_id = self._execute(get_book_id, [title, publisher])[0][0]

        # Add or update the stock at the branch
        get_branch_id = """
            SELECT id FROM library_branch WHERE name = ?;
        """
        branch_id = self._execute(get_branch_id, [branch])[0][0]
        update_stock = """
            INSERT INTO inventory (book_id, branch_id, stock)
            VALUES (?1, ?2, ?3)
            ON CONFLICT (book_id, branch_id) 
            DO UPDATE SET stock = stock + ?3;
        """
        self._execute(update_stock, [book_id, branch_id, stock])

        # Add the book's author - do nothing if the author already
        # already exists for that book
        add_author = """
            INSERT INTO author (name) VALUES (?) ON CONFLICT (name) DO NOTHING
        """
        self._execute(add_author, [author])
        get_author_id = """
            SELECT id FROM author WHERE name = ?
        """
        author_id = self._execute(get_author_id, [author])[0][0]

        add_link = """
            INSERT INTO book_author_link (book_id, author_id) VALUES (?, ?) 
            ON CONFLICT (book_id, author_id) DO NOTHING
        """
        self._execute(add_link, [book_id, author_id])