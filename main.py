import os
import threading
import multiprocessing
from sync_database import SyncDatabase


NUM_OF_ACCESSES = 100
CORRECT_NUM = 10

FILENAME = 'test.db'


def update_val_func(db, key):
    """
    Increments a value in a database multiple times.
    :param db: The database.
    :type db: SyncDatabase
    :param key: The key of the value.
    :type key: Any
    """
    for _ in range(CORRECT_NUM):
        db.set_value(key, db.get_value(key) + 1)


def get_val_func(db, key):
    """
    Reads a value from a database.
    :param db: The database.
    :type db: SyncDatabase
    :param key: The key of the value.
    :type key: Any
    """
    db.get_value(key)


def delete_val_func(db, key):
    """
    Deletes a value from a database.
    :param db: The database.
    :type db: SyncDatabase
    :param key: The key of the value.
    :type key: Any
    """
    db.delete_value(key)


def test_after_populating(db, mode):
    """
    Tests the database after populating it and incrementing every value. The function checks that every value is the
    correct number it should be based on the ``update_val_func()`` function.
    :param db: The database.
    :type db: SyncDatabase
    :param mode: The mode of the database (thread or process) as a string for the printing.
    :type mode: str
    """
    print(f'{mode} database after populating: ', end='')
    print(db.dict)
    for i in range(NUM_OF_ACCESSES):
        assert db.get_value(i) == CORRECT_NUM
    print('All values are correct!')


def test_after_deleting(db, mode):
    """
    Tests the database after deleting every key.
    :param db: The database.
    :type db: SyncDatabase
    :param mode: The mode of the database (thread or process) as a string for the printing.
    :type mode: str
    """
    print(f'{mode} database after deleting: ', end='')
    print(db.dict)
    assert db.dict == {}
    print('All values deleted successfully!')


def test_threads():
    """
    Tests the SyncDatabase thread functionality.
    """
    db = SyncDatabase(FILENAME, False)
    threads = []

    print('Testing thread database...')

    for i in range(NUM_OF_ACCESSES):
        db.set_value(i, 0)

    for i in range(NUM_OF_ACCESSES):
        test_thread = threading.Thread(target=update_val_func, args=(db, i))
        threads.append(test_thread)
        test_thread.start()

        test_thread = threading.Thread(target=get_val_func, args=(db, i))
        threads.append(test_thread)
        test_thread.start()

    for thread in threads:
        thread.join()

    threads.clear()
    test_after_populating(db, 'Thread')

    for i in range(NUM_OF_ACCESSES):
        test_thread = threading.Thread(target=delete_val_func, args=(db, i))
        threads.append(test_thread)
        test_thread.start()

    for thread in threads:
        thread.join()

    test_after_deleting(db, 'Thread')


def test_processes():
    """
    Tests the SyncDatabase process functionality.
    """
    db = SyncDatabase(FILENAME, True)
    processes = []

    print('Testing process database...')

    for i in range(NUM_OF_ACCESSES):
        db.set_value(i, 0)

    for i in range(NUM_OF_ACCESSES):
        test_process = multiprocessing.Process(target=update_val_func, args=(db, i))
        processes.append(test_process)
        test_process.start()

        test_process = multiprocessing.Process(target=get_val_func, args=(db, i))
        processes.append(test_process)
        test_process.start()

    for process in processes:
        process.join()

    processes.clear()
    test_after_populating(db, 'Process')

    for i in range(NUM_OF_ACCESSES):
        test_process = multiprocessing.Process(target=delete_val_func, args=(db, i))
        processes.append(test_process)
        test_process.start()

    for process in processes:
        process.join()

    test_after_deleting(db, 'Process')


def main():
    """
    The main function.
    """
    test_threads()
    os.remove(FILENAME)
    print()
    test_processes()


if __name__ == '__main__':
    main()
