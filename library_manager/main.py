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

    
    def get_list_of_libraries(self):
        """
            Get a complete list of all the libraries managed by this
            catalogue and return them as a string
        """
        query = """
            SELECT * FROM tbl_library_branch
        """
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
        except sqlite3.Error as e:
            print(
                f'An SQL Error for the connection to {self._connection_path} '
                f'occurred when retrieving list of libraries.\n'
                f'Error code is: {e}'
            )
        except Exception as unexpectedException:
            print(
                f'An unexpected error occurred with code: {unexpectedException}'
            )
        return result

