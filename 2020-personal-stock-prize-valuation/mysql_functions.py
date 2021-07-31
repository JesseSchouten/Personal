# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 11:33:27 2020

@author: Jesse
"""

import pymysql
import datetime
import pandas as pd
import os 

def connect_to_mysql_db(host_name,db_name,user,passwd):
    mysql_conn = pymysql.connect(host=host_name,db=db_name, user=user, passwd=passwd)

    return mysql_conn

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

def execute_select_query(mysql_conn, db_name = None, table_name = None, column_names = None,query = None):
    """
    :param column_names str: 
    :param table_name str:
    :param column_names list:
    """
    if query == None:
        query = _create_select_query(db_name, table_name, column_names)
    
    data = pd.read_sql(query,mysql_conn)
        
    return data

def get_columns_of_table(mysql_conn, db_name, table_name):
    """
    return as list
    """
    query = "SELECT COLUMN_NAME AS columns FROM information_schema.columns WHERE table_schema='{}' AND table_name='{}'".format(db_name,table_name)
    
    data = pd.read_sql(query,mysql_conn)
        
    return data['columns'].to_list()


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

def execute_insert_query(mysql_conn,db_name, table_name, column_names,data):
    """
    :param data list: list with tuples in the rows 
    """
    query = _create_insert_query(db_name, table_name, column_names,data)

    mysql_conn_cursor = mysql_conn.cursor()

    nr_executed = mysql_conn_cursor.executemany(query,data)

    mysql_conn.commit()

    mysql_conn_cursor.close()

    return nr_executed

def execute_defined_insert_query(mysql_conn,query):
    """
    :param query list: str with defined query including the new values in the row
    suited for inserting a single row.
    """
    mysql_conn_cursor = mysql_conn.cursor()
    
    nr_executed = mysql_conn_cursor.execute(query)
    
    mysql_conn.commit()
    
    mysql_conn_cursor.close()
    
    return nr_executed


