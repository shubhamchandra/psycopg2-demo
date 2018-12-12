# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 12:23:03 2018

@author: Shubham
"""

import psycopg2
from db import CursorFromConnectionPool, ConnectionPool

class User:
    
    @classmethod
    def initializeConnectionPool(cls):
        ConnectionPool.initialize()
    
    def __init__(self):
        pass
        
    def __init__(self, email, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.id = None
        
    def __repr__(self):
        return  '<User id: {}, email: {}, first_name: {}, last_name: {}>'.format(self.id, self.email, self.first_name, self.last_name)
        
    def save_to_db(self):
        with CursorFromConnectionPool() as cursor:
            cursor.execute('INSERT INTO users (email, first_name, last_name) VALUES (%s, %s, %s)',(self.email, self.first_name, self.last_name))
        
    def set_id(self, id):
        self.id = id
        
    @classmethod
    def load_from_db(cls, email):
        user = cls;
        with CursorFromConnectionPool() as cursor: # returns a new connection
            cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
            user_data = cursor.fetchone()
            user = cls(email=user_data[1], first_name=user_data[2], last_name=user_data[3])
            user.set_id(user_data[0])
            return user
            
            
            
            