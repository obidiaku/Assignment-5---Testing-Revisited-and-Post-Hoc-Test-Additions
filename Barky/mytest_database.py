
import sys
import os
import sqlite3

from abc import ABC, abstractmethod
from datetime import datetime


import requests

import pytest
from database import DatabaseManager
#from mymodule import MyDatabaseClass

# module scope
db = DatabaseManager("bookmarks.db")


@pytest.fixture
def database_manager() -> DatabaseManager:
    filename = "test_bookmarks.db"
    dbm = DatabaseManager(filename)
    # what is yield? https://www.guru99.com/python-yield-return-generator.html
    yield dbm
    dbm.__del__()           # explicitly release the database manager
    os.remove(filename)


def test_execute(database_manager):
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

    # insert test data
    conn = database_manager.connection
    cursor = conn.cursor()
    statement = "INSERT INTO bookmarks (title, url, notes, date_added) VALUES (?, ?, ?, ?)"
    values = ("Test bookmark", "http://www.wtamu.edu",
              "Test notes", "2022-01-01")
    cursor.execute(statement, values)
    conn.commit()

    # assert
    statement = "SELECT * FROM bookmarks WHERE url IS NOT NULL"
    cursor.execute(statement)
    assert cursor.fetchone() is not None

    # cleanup
    database_manager.drop_table("bookmarks")


# testing for deleting file


def test_drop_table(database_manager):
    # Create a table to drop
    database_manager.create_table(
        table_name='bookmarks',
        columns={'id': 'integer', 'name': 'text'}
    )

    # Drop the table
    database_manager.drop_table('bookmarks')

    # Verify that the table no longer exists
    with pytest.raises(sqlite3.OperationalError):
        database_manager._execute('SELECT * FROM bookmarks')


# Define a test function for the add method


class MyDatabaseClass:
    def __init__(self, conn):
        self.conn = conn

    def add(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        cursor = self.conn.cursor()
        cursor.execute(sql, tuple(data.values()))
        self.conn.commit()


def test_add():
    conn = sqlite3.connect(':memory:')
    db = MyDatabaseClass(conn)


# Create the bookmarks table
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE bookmarks (id INTEGER PRIMARY KEY, title TEXT, url TEXT, notes TEXT, date_added TEXT)')
    # Add test data to the database
    data = {
        'title': 'Test Title',
        'url': 'http://example.com',
        'notes': 'Test notes',
        'date_added': '2022-01-01'
    }
    db.add('bookmarks', data)

    # Query the database and verify that the test data was added correctly
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookmarks WHERE title = ?', ('Test Title',))
    result = cursor.fetchone()
    expected = (1, 'Test Title', 'http://example.com',
                'Test notes', '2022-01-01')
    assert result == expected

    # Close the database connection
    conn.close()
