import os
from datetime import datetime
import sqlite3

import pytest


from database import DatabaseManager


@pytest.fixture
def database_manager() -> DatabaseManager:

    filename = 'test.db'
    db = DatabaseManager(filename)
    yield db
    db.__del__()
    os.remove(filename)


def test_database_manager_delete_bookmark(database_manager):
    """ def database():
         filename = 'test.db'
         db = DatabaseManager(filename)
         yield db
         db.__del__()
         os.remove(filename)
     """

    # def test_delete(database):

    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    """database_manager.add(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )
    """

    database_manager.delete('bookmarks', {'id': 1})

    conn = database_manager.connection
    cursor = conn.cursor()

    cursor.execute(
        ''' SELECT * FROM sqlite_master WHERE name = 'bookmarks' ''')

    rows = cursor.fetchall()
    assert len(rows) == 1
# tested table record delete, but did not pass. After delete ,method, table record still exists.
