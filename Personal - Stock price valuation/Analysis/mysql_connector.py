# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 11:13:26 2020

@author: Jesse
"""

import pymysql
import datetime
import pandas as pd
import os 

from File_Logging import FileLogging

current_working_directory = os.getcwd()
file_logging = FileLogging(directory = current_working_directory + '\\Logging\\')

def _create_select_query(db_name,table_name, column_names):
    """
    
    """
    query= "SELECT "
    count = 1
    for column in column_names:
        query += column

        if count != len(column_names):
            query += ', '
        count += 1
    query += ' FROM {}.{}'.format(db_name,table_name)
    return query


def _create_insert_query(db_name,table_name, column_names,column_values,ignore = True):
    """
    ON DUPLICATE KEY UPDATE NOT SUPPORTED
    """

    query = 'INSERT '
    if ignore == True:
        query += 'IGNORE '
    query += 'INTO {}.{} '.format(db_name,table_name)
    query += '('
    count = 1
    for column in column_names:
        query += column
        if count != len(column_names):
            query += ', '
        count += 1
    query += ') '
    query += 'VALUES '
    query += '('
    
    count = 1
    for column in column_names:
        query += '%s'
        if count != len(column_names):
            query += ', '
        count += 1
    query += ')'
    return query

class MySQL_connector:
    def __init__(self):
        self.host_name = 'localhost'
        self.user = 'root'
        self.passwd = 'root'
        self.db_name = 'investing'
        self.mysql_conn = None 
        self.mysql_conn_cursor = None
        
    def open_connection(self):        
        self.mysql_conn = pymysql.connect(host=self.host_name,db=self.db_name, user=self.user, passwd=self.passwd)
        self.mysql_conn_cursor = self.mysql_conn.cursor()
        
    def close_connection(self):
        self.mysql_conn.close()
        self.mysql_conn_cursor.close()
       
    def get_columns_of_table(self,table_name):
        """
        return as list
        """
        query = "SELECT COLUMN_NAME AS columns FROM information_schema.columns WHERE table_schema='{}' AND table_name='{}'".format(self.db_name,table_name)
        
        data = pd.read_sql(query,self.mysql_conn)
            
        return data['columns'].to_list()
    
    def execute_select_query(self,query = None,  table_name = None, column_names = None):
        """
        :param table_name str: 
        :param column_names list:
        :param query str:
        """
        self.open_connection()
        
        if query == None:
            query = _create_select_query(self.db_name, table_name, column_names)
        
        data = pd.read_sql(query,self.mysql_conn)
        
        self.close_connection()
        
        return data
    
    def execute_defined_insert_query(self,query):
        """
        :param query list: str with defined query including the new values in the row
        suited for inserting a single row.
        """
        self.open_connection()
        
        self.mysql_conn_cursor = self.mysql_conn.cursor()
    
        nr_executed = self.mysql_conn_cursor.execute(query)
        
        self.mysql_conn.commit()
        
        self.close_connection()

        return nr_executed