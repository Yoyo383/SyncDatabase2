from file_database import FileDatabase
import multiprocessing
import threading


class SyncDatabase(FileDatabase):
    """
    The sync database class.
    """

    NUM_OF_CLIENTS = 10

    def __init__(self, filename, process_mode):
        """
        Initializes a database from a file. If the file doesn't exist, creates it. Also, specifies the mode of
        the database - processes or threads.
        :param filename: The name of the file.
        :type filename: str
        :param process_mode: The mode of the database. If true, it is in process mode. If false, it is in thread mode.
        :type process_mode: bool
        """
        super().__init__(filename)
        if process_mode:
            self.__semaphore = multiprocessing.Semaphore(self.NUM_OF_CLIENTS)
            self.__write_lock = multiprocessing.Lock()
        else:
            self.__semaphore = threading.Semaphore(self.NUM_OF_CLIENTS)
            self.__write_lock = threading.Lock()

    def acquire_semaphore(self):
        """
        Acquires a semaphore.
        """
        self.__semaphore.acquire()

    def release_semaphore(self):
        """
        Releases a semaphore.
        """
        self.__semaphore.release()

    def acquire_write_lock(self):
        """
        Acquires the write lock.
        """
        self.__write_lock.acquire()

    def release_write_lock(self):
        """
        Releases the write lock.
        :return:
        """
        self.__write_lock.release()

    def acquire_all_semaphores(self):
        """
        Acquires all semaphores. This function blocks until all semaphores are acquired.
        """
        for _ in range(self.NUM_OF_CLIENTS):
            self.acquire_semaphore()

    def release_all_semaphores(self):
        """
        Releases all semaphores.
        """
        for _ in range(self.NUM_OF_CLIENTS):
            self.release_semaphore()

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
        self.acquire_write_lock()
        self.acquire_all_semaphores()
        super().set_value(key, value)
        self.release_all_semaphores()
        self.release_write_lock()

    def get_value(self, key):
        """
        Gets a value from the database.
        :param key: The key.
        :type key: Any
        :return: The value of the key.
        :rtype: Any
        """
        self.acquire_semaphore()
        value = super().get_value(key)
        self.release_semaphore()
        return value

    def delete_value(self, key):
        """
        Deletes a key from the database and returns its value.
        :param key: The key.
        :type key: Any
        :return: The value of the key.
        :rtype: Any
        """
        self.acquire_write_lock()
        self.acquire_all_semaphores()
        value = super().delete_value(key)
        self.release_all_semaphores()
        self.release_write_lock()
        return value
