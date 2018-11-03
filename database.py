import sqlite3
import sys

DATABASE_FILE = ':memory:'
conn = sqlite3.connect(DATABASE_FILE)

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
    CREATE TABLE users (username text PRIMARY KEY UNIQUE NOT NULL);
        
    CREATE TABLE trips (id uuid PRIMARY KEY UNIQUE NOT NULL, username text NOT NULL, origin text NOT NULL, destination text NOT NULL);
    """)
    conn.commit()

init_database()
