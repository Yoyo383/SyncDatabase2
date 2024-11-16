"""
sys.argv[1] = database filename
sys.argv[2] = index
sys.argv[3] = what function to call
"""
import sys
from main import CORRECT_NUM
from sync_database import SyncDatabase


def update_val_func(key):
    """
    Increments a value in a database multiple times.
    :param key: The key of the value.
    :type key: Any
    """
    db = SyncDatabase(sys.argv[1], True)
    for _ in range(CORRECT_NUM):
        db.set_value(key, db.get_value(key) + 1)


def delete_val_func(key):
    """
    Deletes a value from a database.
    :param key: The key of the value.
    :type key: Any
    """
    db = SyncDatabase(sys.argv[1], True)
    db.delete_value(key)


if __name__ == '__main__':
    if sys.argv[3] == 'update':
        update_val_func(int(sys.argv[2]))
    elif sys.argv[3] == 'delete':
        delete_val_func(int(sys.argv[2]))

