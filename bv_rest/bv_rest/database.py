import collections
import threading
import time

from flask import current_app
import psycopg2
import psycopg2.extras


class ConnectionPool:
    class ConnectionRecord:
        def __init__(self, database, creation_time, last_used, connection):
            self.database = database
            self.creation_time = creation_time
            self.last_used = last_used
            self.connection = connection

    def __init__(self, max_connections=6):
        self.lock = threading.RLock()
        self.max_connections = max_connections
        self.free = collections.deque()
        self.free_per_database = {}
        self.in_use = collections.deque()

    def get_connection(self, database):
        with self.lock:
            free = self.free_per_database.get(database)
            if free:
                record = free.popleft()
                record.last_used = time.time()
                self.free.remove(record)
                self.in_use.append(record)
                return record.connection
            elif self.free:
                record = self.free.popleft()
                record.last_used = time.time()
                self.free_per_database[record.database].remove(record)
                self.in_use.append(record)
                return record.connection
            if len(self.in_use) == self.max_connections:
                raise RuntimeError('All database connections are in use')
            connection =  psycopg2.connect(host='bv_postgres',
                                           dbname=database,
                                           user=current_app.postgres_user,
                                           password=current_app.postgres_password)
            record = self.ConnectionRecord(database=database,
                                           creation_time=time.time(),
                                           last_used=time.time(),
                                           connection=connection)
            self.in_use.append(record)
            return record.connection

    def free_connection(self, connection):
        with self.lock:
            for record in self.in_use:
                if record.connection == connection:
                    break
            else:
                record = None
            if record is not None:
                self.in_use.remove(record)
                record.last_used = time.time()
                self.free.append(record)
                self.free_per_database.setdefault(record.database, collections.deque()).append(record)


class WithDatabaseConnection:
    def __init__(self, database):
        self.database = database
    
    def __enter__(self):
        self.connection = current_app.db_pool.get_connection(self.database)
        return self.connection

    def __exit__(self, x, y, z):
        if x is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        current_app.db_pool.free_connection(self.connection)
        self.connection = None


class WithDatabaseCursor:
    def __init__(self, database, as_dict=False):
        self.database = database
        self.as_dict = as_dict
    
    def __enter__(self):
        self.wdb = WithDatabaseConnection(self.database)
        connection = self.wdb.__enter__()
        if self.as_dict:
            self.cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            self.cursor = connection.cursor()
        return self.cursor.__enter__()

    def __exit__(self, x, y, z):
        self.cursor.__exit__(x, y, z)
        self.wdb.__exit__(x, y, z)
        self.wdb = self.cursor = None


def get_db(database):
    return WithDatabaseConnection(database)


def get_cursor(database, as_dict=False):
    return WithDatabaseCursor(database,
                              as_dict=as_dict)


def init_app(app):
    app.db_pool = ConnectionPool()
    app.postgres_user = open('/bv_services/postgres_user').read().strip()
    app.postgres_password=open('/bv_services/postgres_password').read()
