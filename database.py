import sqlite3
import sys

DATABASE_FILE = ':memory:'
conn = sqlite3.connect(DATABASE_FILE)

def logger(f):
    def with_logger(*args, **kwargs):
        print("Executing query", *args, file=sys.stderr)
        return f(*args, **kwargs)
    return with_logger

@logger
def execute(query):
    with conn:
        conn.executescript(query)

@logger
def fetchone(query):
    with conn:
        return conn.execute(query).fetchone()

@logger
def fetchall(query):
    with conn:
        return conn.execute(query).fetchall()

def init_database():
    conn.executescript("""
    CREATE TABLE users (username text PRIMARY KEY UNIQUE NOT NULL, password text NOT NULL, salt text NOT NULL);
    INSERT INTO users VALUES ('test', '52d42704a5b54ab6800cc2385c60c6dc62e80da8e4a98b3c6a28dd1fcaa6015a', 'e5db57d0fd6c4e6fbc4ace161beb855f');

    CREATE TABLE trips (id uuid PRIMARY KEY UNIQUE NOT NULL, username text NOT NULL, origin text NOT NULL, destination text NOT NULL, seats int NOT NULL);

    CREATE TABLE carpools (id uuid NOT NULL, username text NOT NULL);
    """)
    conn.commit()

init_database()
