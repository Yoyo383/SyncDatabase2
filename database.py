class Database:
    """
    The basic database class.
    """

    def __init__(self):
        """
        Initializes an empty database.
        """
        self._db = {}

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
        self._db[key] = value
        return True

    def get_value(self, key):
        """
        Gets a value from the database.
        :param key: The key.
        :type key: Any
        :return: The value of the key.
        :rtype: Any
        """
        if key in self._db.keys():
            return self._db[key]
        return None

    def delete_value(self, key):
        """
        Deletes a key from the database and returns its value.
        :param key: The key.
        :type key: Any
        :return: The value of the key.
        :rtype: Any
        """
        if key not in self._db.keys():
            return None
        value = self._db[key]
        del self._db[key]
        return value

    @property
    def dict(self):
        """
        Returns the dictionary as read-only.
        :return: The dictionary of the database.
        :rtype: dict
        """
        return self._db
