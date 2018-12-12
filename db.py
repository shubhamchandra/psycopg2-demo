# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 13:34:15 2018

@author: Shubham
"""

from psycopg2 import pool

class ConnectionPool:
    #class variable => shared by all objects, singleton
    __connection_pool = None
    # __variable makes it private and unaccessible outside class
    
    '''
        With staticmethod you need to access the class variables / static variables
        by Classname.variable, but with classmethod you can do it in a generic way -
        cls.variable
        both classmethods and staticmethods can be called by Classname.method()
    '''
    
    @classmethod
    def initialize(cls):
        cls.__connection_pool = pool.SimpleConnectionPool(1,
                                                1,
                                                database='Student',
                                                user='postgres',
                                                password='root',
                                                host='localhost')
    
    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()
        
    @classmethod
    def put_connection(cls, connection):
        cls.__connection_pool.putconn(connection)
        
    @classmethod
    def close_all_connections(cls):
        cls.__connection_pool.closeall()
        
class CursorFromConnectionPool:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    # with construct entry point
    def __enter__(self):
        self.connection =  ConnectionPool.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor
    
    # with construct exit point
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val != None:
            self.connection.rollback();
        else:
            self.connection.commit()
        self.cursor.close()
        ConnectionPool.put_connection(self.connection)
    
    