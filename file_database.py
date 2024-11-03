from database import Database
import pickle
import os


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

        if os.path.isfile(filename):
            self.load_from_file()
        else:
            self.write_to_file()

    def load_from_file(self):
        """
        Loads the database from the file.
        """
        with open(self.filename, 'rb') as file:
            self._db = pickle.load(file)

    def write_to_file(self):
        """
        Writes the database to the file.
        """
        with open(self.filename, 'wb') as file:
            pickle.dump(self._db, file)

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
