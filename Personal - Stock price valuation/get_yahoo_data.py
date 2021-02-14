# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 13:57:04 2020

@author: Jesse

To do:
    - Use tickers_dow() and tickers_other() to Map all tickers to indices in db.
    - Discounted cash flow and intrinsic value analysis?
"""

"""

Format of stock dict: 
    - ticker:comment
"""

import argparse
import os
import sys
import datetime
import copy
import warnings
warnings.filterwarnings("ignore")

import yahoo_fin.stock_info  as yf #https://github.com/atreadw1492/yahoo_fin
import pandas as pd
import numpy as np
import yahoofinance as yf2
from yahoofinancials import YahooFinancials
import yfinance as yf3

#Import manual modules
from File_Logging import FileLogging
import mysql_functions 

def profile_to_csv(ticker):
    profile = yf2.AssetProfile(ticker)
    try:
        profile.to_csv("Companies/" + ticker + '-profile.csv')
    except Exception as e:
        file_logging.logger.error('Couldnt write profile to csv: ' + str(e))
    return

def profile_info_from_csv(ticker,index_ticker):
    try:
        data = pd.read_csv('Companies/' + ticker + '-profile.csv',sep='\t',encoding='unicode_escape')
        country = data['Profile'].loc[3].split(',')[1]
        sector = data['Profile'].loc[6].split(',')[1]
        industry = data['Profile'].loc[7].split(',')[1]
        fte = data['Profile'].loc[8].split(',')[1]
        row_dict={'ticker':ticker
            , 'index_ticker':index_ticker
              ,'country':country
              , 'sector':sector
              , 'industry':industry
              , 'fte':fte
              }
    except Exception as e:
        row_dict={}
        file_logging.logger.error('Couldnt read profile from csv: ' + str(e))
    
    return row_dict
    
def profile_info_to_df(tickers,index_tickers):
    global file_logging
    df = pd.DataFrame(columns = ['ticker','country','sector','industry','fte'])
    
    for ticker,index_ticker in zip(tickers,index_tickers):
        file_logging.logger.info("Starting loading profile info of company " + ticker)
        try:
            profile_to_csv(ticker)
            row_dict = profile_info_from_csv(ticker,index_ticker)
        except (KeyError,UnicodeEncodeError,PermissionError) as e:
            row_dict={'ticker':ticker
            ,'index_ticker':index_ticker
          ,'country':None
          , 'sector':None
          , 'industry':None
          , 'fte':None
          }
            file_logging.logger.error('Known error in profile_info_to_df: ' + str(e))
            continue
        except Exception as e:
            row_dict={'ticker':ticker
            ,'index_ticker':index_ticker
          ,'country':None
          , 'sector':None
          , 'industry':None
          , 'fte':None
          }
            file_logging.logger.error('Unknown error in profile_info_to_df: ' + str(e))
            continue
        df = df.append(row_dict,ignore_index=True)
    return df

def fill_company_table(table_column_dict,tickers,index_tickers,mysql_conn):
    global db_name
    global file_logging
    file_logging.logger.info("Started fill_company_table")
    
    table_name = 'company'
  
    table_columns = copy.copy(table_column_dict[table_name])
    table_columns.remove('id')
    
    companies = profile_info_to_df(tickers,index_tickers)
    
    companies['created'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    companies['updated'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    companies_dict = companies[table_columns].values.tolist()   

    try:
        mysql_functions.execute_insert_query(mysql_conn,db_name, table_name, table_columns,companies_dict)
    except Exception as e:
        file_logging.logger.error('Error in fill_company_table: ' + str(e))
        
    return

def get_db_table_columns(database_dict,mysql_conn):
    global file_logging
    
    table_column_dict = {}
    for db,tables in database_dict.items():
        table_dict= {}
        for table in tables:
            columns = mysql_functions.get_columns_of_table(mysql_conn, db, table)
            table_dict[table] = columns
        table_column_dict[db] = table_dict
    return table_column_dict

def read_stock_file(file_name,return_tickers_only = True):
    global file_logging
    
    stock_df = pd.read_csv(file_name)
    if return_tickers_only == True:
        return stock_df['ticker'].to_list(),stock_df['index_ticker'].to_list()
    else:
        return stock_df

def convertStrToNumber(x):
    m = {'K': 3, 'M': 6, 'B': 9, 'T': 12,'%':0.01}

    try:
        if x[:-1] =='%':
            result = round(float(x[:-1]) * m[x[-1]],2)
        else:
            result = int(float(x[:-1]) * 10 ** m[x[-1]])
    except Exception:
        result = x
    return result

def fill_stats_table(table_column_dict,ticker,mysql_conn):
    global db_name
    global file_logging
    
    file_logging.logger.info("Started fill_stats_table")
    
    table_name = 'stats'
  
    table_columns = copy.copy(table_column_dict[table_name])
    table_columns.remove('id')
    try:
        stats = yf.get_stats(ticker)
        stats.columns = map(str.lower, stats.columns)
        stats = stats.where(pd.notnull(stats), None)
        stats['ticker'] = ticker
        stats['date'] = datetime.date.today()
        stats['created'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stats['updated'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        stats['value'] = stats['value'].apply(lambda x: convertStrToNumber(x) )
    
        stats_dict = stats[table_columns].values.tolist()   
    
        try:
             mysql_functions.execute_insert_query(mysql_conn,db_name, table_name, table_columns,stats_dict)
        except Exception as e:
            file_logging.logger.error(e)
    except ValueError:
        file_logging.logger.warning(ticker + " failed loading stats due to known error.  Might indicate mistake in stock ticker.")
    return


def fill_pricing_table(table_column_dict,ticker,mysql_conn):
    global db_name
    global file_logging
    
    file_logging.logger.info("Started fill_pricing_table")
    
    table_name = 'pricing'
  
    table_columns = copy.copy(table_column_dict[table_name])
    table_columns.remove('id')
    try:
        pricing = yf.get_data(ticker)
        pricing = pricing.reset_index().rename(columns={'index':'date'})
        pricing['date'] = pricing['date'].apply(lambda x: str(x.date()))
        pricing.columns = map(str.lower, pricing.columns)
        pricing['created'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pricing['updated'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        pricing_dict = pricing[table_columns].values.tolist()   
    
        try:
             mysql_functions.execute_insert_query(mysql_conn,db_name, table_name, table_columns,pricing_dict)
        except Exception as e:
            file_logging.logger.error('Error in fill_pricing_table: ' + str(e))
    except ValueError:
        file_logging.logger.warning(ticker + " failed loading stats due to known error. Might indicate mistake in stock ticker.")
    except AssertionError:
        file_logging.logger.warning(ticker + " failed loading stats due to known error.  Might indicate mistake in stock ticker.")
    return

def prepare_quarterly_income_statement_table(data):
    df_list=[]
    for key,value in data['incomeStatementHistoryQuarterly'].items():
        if value != None:
            for quarter in value:
                start_df=pd.DataFrame.from_dict(quarter, orient='index').T.reset_index()
                cols = start_df.columns.tolist()
                col_1 = cols.pop(0)
                col_2 = cols.pop(0)
                selected_cols =[]
                selected_cols.append(col_1)
                selected_cols.append(col_2)
                df = start_df[selected_cols]
                try:
                    df['period'] = datetime.datetime.strptime(col_2, "%m/%d/%Y").strftime("%Y-%m-%d")
                except:
                    df['period'] = col_2
                df = df.rename(columns={col_2:'value',col_1:'attribute'})
                df = df[['period', 'attribute','value']]
                df_list.append(df)
            result = pd.concat(df_list)
            break
        else:
            result = pd.DataFrame(columns = ['period', 'attribute','value'])

    return result


def prepare_income_statement_table(data):
    cols = data.columns.tolist()
    col_1 = cols.pop(0)
    df_list=[]
    for col in cols:
        selected_cols =[]
        selected_cols.append(col_1)
        selected_cols.append(col)
        df = data[selected_cols]
        try:
            df['period'] = datetime.datetime.strptime(col, "%m/%d/%Y").strftime("%Y")
        except:
            df['period'] = col
        df = df.rename(columns={col:'value',col_1:'attribute'})
        df = df[['period', 'attribute','value']]
        df_list.append(df)
    result = pd.concat(df_list)
    
    return result
    
def fill_income_statement_table(table_column_dict,ticker,mysql_conn):
    global db_name
    global file_logging
    
    file_logging.logger.info("Started fill_income_statement_table")
    
    table_name = 'income_statement'
  
    table_columns = copy.copy(table_column_dict[table_name])
    table_columns.remove('id')
  
    data = yf.get_income_statement(ticker) #https://finance.yahoo.com/quote/NFLX/financials?p=NFLX
    try:
        income_statement =prepare_income_statement_table(data)
        
        income_statement = income_statement.where(pd.notnull(income_statement), None)
        income_statement['ticker'] = ticker
        income_statement['date'] = datetime.date.today()
        income_statement['created'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        income_statement['updated'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        income_statement_dict = income_statement[table_columns].values.tolist()   
        
        try:
             mysql_functions.execute_insert_query(mysql_conn,db_name, table_name, table_columns,income_statement_dict)
        except Exception as e:
            file_logging.logger.error('Error in fill_income_statement_table: ' + str(e))
    except IndexError:
        file_logging.logger.warning(ticker + " failed loading income statement due to known error.  Might indicate mistake in stock ticker.")
    
    pre_data = YahooFinancials(ticker)
    data_quarterly = pre_data.get_financial_stmts(frequency = 'quarterly', statement_type = 'income')
  
    try: 
        income_statement_quarterly = prepare_quarterly_income_statement_table(data_quarterly)

        income_statement_quarterly = income_statement_quarterly.where(pd.notnull(income_statement_quarterly), None)
        income_statement_quarterly['ticker'] = ticker
        income_statement_quarterly['date'] = datetime.date.today()
        income_statement_quarterly['created'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        income_statement_quarterly['updated'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        income_statement_quarterly_dict = income_statement_quarterly[table_columns].values.tolist()   

        try:
             mysql_functions.execute_insert_query(mysql_conn,db_name, table_name, table_columns,income_statement_quarterly_dict)
        except Exception as e:
            file_logging.logger.error('Error in fill_income_statement_table (quarterly data): ' + str(e))
    except IndexError:
        file_logging.logger.warning(ticker + " failed loading income statement (quarterly) due to known error.  Might indicate mistake in stock ticker.")
 
    return

def prepare_quarterly_balance_sheet_table(data):
    df_list=[]
    for key,value in data['balanceSheetHistoryQuarterly'].items():
        if value != None:
            for quarter in value:
                start_df=pd.DataFrame.from_dict(quarter, orient='index').T.reset_index()
                cols = start_df.columns.tolist()
                col_1 = cols.pop(0)
                col_2 = cols.pop(0)
                selected_cols =[]
                selected_cols.append(col_1)
                selected_cols.append(col_2)
                df = start_df[selected_cols]
                try:
                    df['period'] = datetime.datetime.strptime(col_2, "%m/%d/%Y").strftime("%Y-%m-%d")
                except:
                    df['period'] = col_2
                df = df.rename(columns={col_2:'value',col_1:'attribute'})
                df = df[['period', 'attribute','value']]
                df_list.append(df)
            result = pd.concat(df_list)
            break
        else:
            result = pd.DataFrame(columns = ['period', 'attribute','value'])

    return result

def prepare_balance_sheet_table(data):
    cols = data.columns.tolist()
    col_1 = cols.pop(0)
    df_list=[]
    for col in cols:
        selected_cols =[]
        selected_cols.append(col_1)
        selected_cols.append(col)
        df = data[selected_cols]
        try:
            df['period'] = datetime.datetime.strptime(col, "%m/%d/%Y").strftime("%Y")
        except:
            df['period'] = col
        df = df.rename(columns={col:'value',col_1:'attribute'})
        df = df[['period', 'attribute','value']]
        df_list.append(df)
    result = pd.concat(df_list)
    
    return result
    
def fill_balance_sheet_table(table_column_dict,ticker,mysql_conn):
    global db_name
    global file_logging
    
    file_logging.logger.info("Started fill_balance_sheet_table")
    
    table_name = 'balance_sheet'
  
    table_columns = copy.copy(table_column_dict[table_name])
    table_columns.remove('id')
  
    data = yf.get_balance_sheet(ticker) #https://finance.yahoo.com/quote/NFLX/financials?p=NFLX
    try:
        balance_sheet =prepare_balance_sheet_table(data)
              
        balance_sheet=balance_sheet.where(pd.notnull(balance_sheet), None)
        balance_sheet['ticker'] = ticker
        balance_sheet['date'] = datetime.date.today()
        balance_sheet['created'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        balance_sheet['updated'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        balance_sheet_dict = balance_sheet[table_columns].values.tolist()   
        
        try:
             mysql_functions.execute_insert_query(mysql_conn,db_name, table_name, table_columns,balance_sheet_dict)
        except Exception as e:
            file_logging.logger.error('Error in fill_balance_sheet_table: ' + str(e))
    except IndexError:
        file_logging.logger.warning(ticker + " failed loading balance sheet data due to known error.  Might indicate mistake in stock ticker.")
    pre_data = YahooFinancials(ticker)
    data_quarterly = pre_data.get_financial_stmts(frequency = 'quarterly', statement_type = 'balance')
   
    try:
        balance_sheet_quarterly =prepare_quarterly_balance_sheet_table(data_quarterly)
        
        balance_sheet_quarterly.where(pd.notnull(balance_sheet_quarterly), None)
        balance_sheet_quarterly['ticker'] = ticker
        balance_sheet_quarterly['date'] = datetime.date.today()
        balance_sheet_quarterly['created'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        balance_sheet_quarterly['updated'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        balance_sheet_quarterly_dict = balance_sheet_quarterly[table_columns].values.tolist()   

        try:
             mysql_functions.execute_insert_query(mysql_conn,db_name, table_name, table_columns,balance_sheet_quarterly_dict)
        except Exception as e:
            file_logging.logger.error('Error in fill_balance_sheet_table (quarterly data): ' + str(e))
    except IndexError:
        file_logging.logger.warning(ticker + " failed loading balance sheet data due to known error.  Might indicate mistake in stock ticker.")

    return

def prepare_quarterly_cashflow_table(data):
    df_list=[]
    for key,value in data['cashflowStatementHistoryQuarterly'].items():
        if value != None:
            for quarter in value:
                
                start_df=pd.DataFrame.from_dict(quarter, orient='index').T.reset_index()
                cols = start_df.columns.tolist()
                col_1 = cols.pop(0)
                col_2 = cols.pop(0)
                selected_cols =[]
                selected_cols.append(col_1)
                selected_cols.append(col_2)
                df = start_df[selected_cols]
                try:
                    df['period'] = datetime.datetime.strptime(col_2, "%m/%d/%Y").strftime("%Y-%m-%d")
                except:
                    df['period'] = col_2
                df = df.rename(columns={col_2:'value',col_1:'attribute'})
                df = df[['period', 'attribute','value']]
                df_list.append(df)
            result = pd.concat(df_list)
            break
        else:
            result = pd.DataFrame(columns = ['period', 'attribute','value'])
    return result

def prepare_cashflow_table(data):
    cols = data.columns.tolist()
    col_1 = cols.pop(0)
    df_list=[]
    for col in cols:
        selected_cols =[]
        selected_cols.append(col_1)
        selected_cols.append(col)
        df = data[selected_cols]
        try:
            df['period'] = datetime.datetime.strptime(col, "%m/%d/%Y").strftime("%Y")
        except:
            df['period'] = col
        df = df.rename(columns={col:'value',col_1:'attribute'})
        df = df[['period', 'attribute','value']]
        df_list.append(df)
    result = pd.concat(df_list)
    
    return result
    
def fill_cashflow_table(table_column_dict,ticker,mysql_conn):
    global db_name
    global file_logging
    
    file_logging.logger.info("Started fill_cashflow_table")
    
    table_name = 'cashflow'
  
    table_columns = copy.copy(table_column_dict[table_name])
    table_columns.remove('id')
  
    data = yf.get_cash_flow(ticker) #https://finance.yahoo.com/quote/NFLX/financials?p=NFLX
    try:
        cashflow =prepare_cashflow_table(data)
        cashflow=cashflow.where(pd.notnull(cashflow), None)
        cashflow['ticker'] = ticker
        cashflow['date'] = datetime.date.today()
        cashflow['created'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cashflow['updated'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cashflow_dict = cashflow[table_columns].values.tolist()   

        try:
            mysql_functions.execute_insert_query(mysql_conn,db_name, table_name, table_columns,cashflow_dict)
        except Exception as e:
            file_logging.logger.error('Error in fill_cashflow_table: ' + str(e))
    except IndexError:
        file_logging.logger.warning(ticker + " failed loading cashflow data due to known error.  Might indicate mistake in stock ticker.")
   
    pre_data = YahooFinancials(ticker)
    data_quarterly = pre_data.get_financial_stmts(frequency = 'quarterly', statement_type = 'cash')

    try:
        cashflow_quarterly =prepare_quarterly_cashflow_table(data_quarterly)

        cashflow_quarterly.where(pd.notnull(cashflow_quarterly), None)
        cashflow_quarterly['ticker'] = ticker
        cashflow_quarterly['date'] = datetime.date.today()
        cashflow_quarterly['created'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cashflow_quarterly['updated'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cashflow_quarterly_dict = cashflow_quarterly[table_columns].values.tolist()   
        try:
             mysql_functions.execute_insert_query(mysql_conn,db_name, table_name, table_columns,cashflow_quarterly_dict)
        except Exception as e:
            file_logging.logger.error('Error in fill_cashflow_table (quarterly data): ' + str(e))
    except IndexError:
        file_logging.logger.warning(ticker + " failed loading cashflow data due to known error.  Might indicate mistake in stock ticker.")

def prepare_analysts_table(data):
    cols = data.columns.tolist()
    col_1 = cols.pop(0)
    df_list=[]
    for col in cols:
        selected_cols =[]
        selected_cols.append(col_1)
        selected_cols.append(col)
        df = data[selected_cols]
        try:
            df['description'] = datetime.datetime.strptime(col, "%m/%d/%Y").strftime("%Y-%m-%d")
        except:
            df['description'] = col
        df = df.rename(columns={col_1:'attribute',col:'value'})
        df = df[['description', 'attribute','value']]
        df_list.append(df)
    result = pd.concat(df_list)
    
    return result

def fill_analysts_table(table_column_dict,ticker,mysql_conn):
    global db_name
    global file_logging
    
    file_logging.logger.info("Started fill_analysts_table")
    
    table_name = 'analysts_estimates'
  
    table_columns = copy.copy(table_column_dict[table_name])
    table_columns.remove('id')
  
    data = yf.get_analysts_info(ticker) #https://finance.yahoo.com/quote/NFLX/financials?p=NFLX
    for key,df_data in data.items():
        try:
            analysts_data =prepare_analysts_table(df_data)
          
            analysts_data=analysts_data.where(pd.notnull(analysts_data), None)
            analysts_data['ticker'] = ticker
            analysts_data['date'] = datetime.date.today()
            analysts_data['created'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            analysts_data['updated'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            analysts_data_list = analysts_data[table_columns].values.tolist()   
        
            try:
                 mysql_functions.execute_insert_query(mysql_conn,db_name, table_name, table_columns,analysts_data_list)
            except Exception as e:
                file_logging.logger.error('Error in fill_analysts_table: ' + str(e))
        except IndexError:
            file_logging.logger.warning(ticker + " failed loading balance sheet data due to known error.  Might indicate mistake in stock ticker.")
    return

def main(load_company_table = False,load_daily_stats = True, load_pricing_ts= False,load_yearly_data = False,load_analysts_data = False,to_csv=False):
    global database_dict
    global file_logging
    global stock_file
    global db_name
    
    file_logging.logger.info("Starting main.")
    file_logging.logger.info("Load company table: " + str(load_company_table))
    file_logging.logger.info("Load daily stats: " + str(load_daily_stats))
    file_logging.logger.info("Load stock time series data: " + str(load_pricing_ts))
    file_logging.logger.info("Balance sheets, etc (yearly/ quarterly data): " + str(load_yearly_data))
    file_logging.logger.info("Analysts data: " + str(load_analysts_data))
    
    
    host_name = 'localhost'
    user = 'root'
    passwd = 'root'
    
    mysql_conn = mysql_functions.connect_to_mysql_db(host_name,db_name,user,passwd)
 
    table_column_dict = get_db_table_columns(database_dict,mysql_conn)[db_name]

    tickers,index_tickers = read_stock_file(stock_file)
    
    try:
        if load_company_table == True:
            fill_company_table(table_column_dict,tickers,index_tickers,mysql_conn)
    except Exception as e:
        file_logging.logger.error('Error in fill_company_table: ' + str(e))
    
    for ticker in tickers:
        file_logging.logger.info("Processing ticker {}".format(ticker))
        
        try:
            if load_daily_stats == True:
                fill_stats_table(table_column_dict,ticker,mysql_conn)
        except Exception as e:
            file_logging.logger.error('Error in fill_stats_table: ' + str(e) + ' at ticker ' + str(ticker))
            
        try:
            if load_pricing_ts == True:
                fill_pricing_table(table_column_dict,ticker,mysql_conn)
        except Exception as e:
            file_logging.logger.error('Error in fill_pricing_table: ' + str(e) + ' at ticker ' + str(ticker))
         
        try:
            if load_yearly_data == True:
                fill_income_statement_table(table_column_dict,ticker,mysql_conn)
        except Exception as e:
            file_logging.logger.error('Error in fill_income_statement_table: ' + str(e) + ' at ticker ' + str(ticker))
            
        try:
            if load_yearly_data == True:
                fill_balance_sheet_table(table_column_dict,ticker,mysql_conn)
        except Exception as e:
            file_logging.logger.error('Error in fill_balance_sheet_table: ' + str(e) + ' at ticker ' + str(ticker))
            
        try:
            if load_yearly_data == True:
                fill_cashflow_table(table_column_dict,ticker,mysql_conn)
        except Exception as e:
            file_logging.logger.error('Error in fill_cashflow_table: ' + str(e) + ' at ticker ' + str(ticker))
            
        try:
            if load_analysts_data == True:
                fill_analysts_table(table_column_dict,ticker,mysql_conn)
        except Exception as e:
            file_logging.logger.error('Error in fill_analysts_table: ' + str(e) + ' at ticker ' + str(ticker))
           
     
      
"""
t1 = yf.get_data("NFLX") 

t2 = yf.get_quote_table("NFLX") #https://finance.yahoo.com/quote/NFLX?p=NFLX


t4 = yf.get_income_statement("NFLX") #https://finance.yahoo.com/quote/NFLX/financials?p=NFLX

t5 = yf.get_balance_sheet("NFLX") #https://finance.yahoo.com/quote/NFLX/balance-sheet?p=NFLX

t6 = yf.get_cash_flow("NFLX") # https://finance.yahoo.com/quote/NFLX/cash-flow?p=NFLX

t7 = yf.get_holders("NFLX") #https://finance.yahoo.com/quote/NFLX/holders?p=NFLX

t8 = yf.get_analysts_info("NFLX") # https://finance.yahoo.com/quote/NFLX/analysts?p=NFLX

t9 = yf.get_top_crypto()
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Gets data from yahoo.finance")

    parser.add_argument(
        "--working_directory",
        default = 'C:/Users/Jesse/OneDrive/Bureaublad laptop Jesse/Beleggen/data/',
        help="working directory of main script",
    )
    
    parser.add_argument(
        "--load_company_table",
        default = False,
        help="Boolean whether daily statistics should be retrieved or not.",
    )
    
    parser.add_argument(
        "--load_daily_stats",
        default = False,
        help="Boolean whether daily statistics should be retrieved or not.",
    )
    
    parser.add_argument(
        "--load_stock_pricing_ts",
        default = False,
        help="Boolean whether stock data should be written to database or not",
    )
    
    parser.add_argument(
        "--load_yearly_data",
        default = False,
        help="Boolean whether yearly or quarterly stockdata should be imported, currently this is balance sheet data and income statement data.",
    )
    
    parser.add_argument(
        "--load_analysts_data",
        default = False,
        help="Boolean whether analysts estimates data should be retrieved to analyst_estimates tables.",
    )

    parser.add_argument(
        "--stock_file_name",
        default = 'all_stocks.csv',
        help="Name of the file that contains the stock tickers in csv format.",
    )


    args = parser.parse_args()

    working_directory = args.working_directory
    
    load_company_table = bool(args.load_company_table)
    
    load_daily_stats = bool(args.load_daily_stats)
    
    load_pricing_ts = bool(args.load_stock_pricing_ts)
    
    load_yearly_data = bool(args.load_yearly_data)
    
    load_analysts_data = bool(args.load_analysts_data)
    
    stock_file = args.stock_file_name
    
    os.chdir(working_directory)
    
    #Global variables
    file_logging = FileLogging(directory=working_directory)
    db_name = 'investing'
    database_dict = {'investing':['company','stats','errors','pricing','income_statement','balance_sheet','cashflow','analysts_estimates']
    ,'investing_short_term':['company','stats','errors','pricing','income_statement','balance_sheet', 'cashflow','analysts_estimates']}

    main(load_company_table=load_company_table,load_daily_stats = load_daily_stats, load_pricing_ts = load_pricing_ts, load_yearly_data = load_yearly_data,load_analysts_data=load_analysts_data)
    
    
    
    
