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

    
    def get_all_libraries(self):
        """
            Get a complete list of all the libraries managed by this
            catalogue and return them as a dictionary
        """
        query = """
            SELECT * FROM tbl_library_branch;
        """
        cursor = self.connection.cursor()
        result_raw = None
        try:
            cursor.execute(query)
            result_raw = cursor.fetchall()
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
        
        if not result_raw:
            return
        
        result_processed = dict()
        for row in result_raw:
            primary_key = row[0]
            library_branch_BranchName = row[1]
            library_branch_BranchAddress = row[2]
            result_processed.update({
                primary_key: {
                    'library_branch_BranchName': library_branch_BranchName,
                    'library_branch_BranchAddress': library_branch_BranchAddress
                    }
                })
        return result_processed