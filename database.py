import sqlite3
import sys

from functools import wraps

DATABASE_FILE = ':memory:'
conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)


def execute(query):
    with conn:
        conn.executescript(query)


def fetchone(query):
    with conn:
        return conn.execute(query).fetchone()


def fetchall(query):
    with conn:
        return conn.execute(query).fetchall()


def init_database():
    conn.executescript("""
        CREATE TABLE users (username text PRIMARY KEY UNIQUE NOT NULL, password text NOT NULL, salt text NOT NULL);

        CREATE TABLE trips (id uuid PRIMARY KEY UNIQUE NOT NULL, username text NOT NULL, origin text NOT NULL, originLat decimal NOT NULL, originLng decimal NOT NULL, destination text NOT NULL, destinationLat decimal NOT NULL, destinationLng decimal NOT NULL, seats int NOT NULL, fare decimal NOT NULL, date date NOT NULL, time time NOT NULL);

        CREATE TABLE carpools (id uuid NOT NULL, username text NOT NULL);
    """)
    conn.commit()


init_database()
