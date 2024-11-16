import win32security

from database import Database
import pickle
import os
import win32file


class FileDatabase(Database):
    """
    The file database class.
    """

    def __init__(self, filename):
        """
        Initializes a database from a file. If the file doesn't exist, creates it.
        :param filename: The name of the file.
        :type filename: str
        """
        super().__init__()
        self.filename = filename
        self.security_attributes = win32security.SECURITY_ATTRIBUTES()
        self.security_attributes.bInheritHandle = True

        if os.path.isfile(filename):
            self.load_from_file()
        else:
            self.write_to_file()

    def load_from_file(self):
        """
        Loads the database from the file.
        """
        file = win32file.CreateFile(
            self.filename, win32file.GENERIC_READ, win32file.FILE_SHARE_READ, None, win32file.OPEN_ALWAYS, 0, 0
        )
        hr, data = win32file.ReadFile(file, win32file.GetFileSize(file))
        win32file.CloseHandle(file)
        self._db = pickle.loads(data)

    def write_to_file(self):
        """
        Writes the database to the file.
        """
        file = win32file.CreateFile(
            self.filename, win32file.GENERIC_WRITE, win32file.FILE_SHARE_READ, None, win32file.OPEN_ALWAYS, 0, 0
        )
        win32file.WriteFile(file, pickle.dumps(self._db))
        win32file.CloseHandle(file)

    def set_value(self, key, value):
        """
        Sets a key to a value.
        :param key: The key.
        :type key: Any
        :param value: The value.
        :type value: Any
        :return: Whether the function was successful.
        :rtype: bool
        """
        self.load_from_file()
        super().set_value(key, value)
        self.write_to_file()

    def get_value(self, key):
        """
        Gets a value from the database.
        :param key: The key.
        :type key: Any
        :return: The value of the key.
        :rtype: Any
        """
        self.load_from_file()
        return super().get_value(key)

    def delete_value(self, key):
        """
        Deletes a key from the database and returns its value.
        :param key: The key.
        :type key: Any
        :return: The value of the key.
        :rtype: Any
        """
        self.load_from_file()
        value = super().delete_value(key)
        self.write_to_file()
        return value

    @property
    def dict(self):
        """
        Returns the dictionary as read-only.
        :return: The dictionary of the database.
        :rtype: dict
        """
        self.load_from_file()
        return self._db
