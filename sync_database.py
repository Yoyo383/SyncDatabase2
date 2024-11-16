import win32api
import win32event
import win32security
from file_database import FileDatabase


class SyncDatabase(FileDatabase):
    """
    The sync database class.
    """

    NUM_OF_CLIENTS = 10
    SEMAPHORE_NAME = 'WriteSemaphore'
    WRITE_LOCK_NAME = 'WriteLock'

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
        security_attributes = win32security.SECURITY_ATTRIBUTES()
        security_attributes.bInheritHandle = True
        self.__semaphore = win32event.CreateSemaphore(None, self.NUM_OF_CLIENTS, self.NUM_OF_CLIENTS, self.SEMAPHORE_NAME)
        self.__write_lock = win32event.CreateMutex(None, False, self.WRITE_LOCK_NAME)

    def __del__(self):
        win32api.CloseHandle(self.__semaphore)
        win32api.CloseHandle(self.__write_lock)

    def acquire_semaphore(self):
        """
        Acquires a semaphore.
        """
        win32event.WaitForSingleObject(self.__semaphore, -1)

    def release_semaphore(self):
        """
        Releases a semaphore.
        """
        win32event.ReleaseSemaphore(self.__semaphore, 1)

    def acquire_write_lock(self):
        """
        Acquires the write lock.
        """
        win32event.WaitForSingleObject(self.__write_lock, -1)

    def release_write_lock(self):
        """
        Releases the write lock.
        :return:
        """
        win32event.ReleaseMutex(self.__write_lock)

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
