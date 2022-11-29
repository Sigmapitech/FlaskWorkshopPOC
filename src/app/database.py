import os
from typing import Generator

import mysql.connector

from contextlib import contextmanager
from mysql.connector.cursor import MySQLCursor


@contextmanager
def open_cursor() -> Generator[MySQLCursor, None, None]:
    cnx = mysql.connector.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
    )
    cursor = cnx.cursor()
    yield cursor
    cnx.commit()
    cursor.close()
