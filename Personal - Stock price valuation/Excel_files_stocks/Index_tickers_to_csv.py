# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:59:14 2020

@author: Jesse
"""
import yahoo_fin.stock_info as yf
import pandas as pd
import ftplib
import io
import re
import datetime
from pytickersymbols import PyTickerSymbols #https://pypi.org/project/pytickersymbols/

# supported tickers of indices from different parts of the world
dutch_indices = ['AEX', 'AMX']
german_indices = ['DAX']
gb_indices =['FTSE100']
french_indices = ['CAC']
usa_indices = ['DJI','GSPC','IXIC']
japanese_indices =['N225']
chinese_indices = []

european_indices = dutch_indices + german_indices + gb_indices
north_american_indices = usa_indices
asian_indices = japanese_indices + chinese_indices 

def tickers_nasdaq():
    
    '''Downloads list of tickers currently listed in the NASDAQ'''
    
    ftp = ftplib.FTP("ftp.nasdaqtrader.com")
    ftp.login()
    ftp.cwd("SymbolDirectory")
    
    r = io.BytesIO()
    ftp.retrbinary('RETR nasdaqlisted.txt', r.write)
    
    info = r.getvalue().decode()
    splits = info.split("|")
    
    tickers = [x for x in splits if "N\r\n" in x]
    tickers = [x.strip("N\r\n") for x in tickers if 'File' not in x]
    
    tickers = sorted(list(set(tickers)))
    
    ftp.close()    

    return tickers

def tickers_dow(): #DJI
    
    '''Downloads list of currently traded tickers on the Dow'''

    site = "https://finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI"
    
    table = pd.read_html(site)[0]

    dow_tickers = sorted(table['Symbol'].tolist())
    
    return dow_tickers

def tickers_sp500(): #GSPC
    '''Downloads list of tickers currently listed in the S&P 500 '''
    # get list of all S&P 500 stocks
    sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    sp_tickers = sorted(sp500.Symbol.tolist())
    
    return sp_tickers


def tickers_other():
    '''Downloads list of tickers currently listed in the "otherlisted.txt"
       file on "ftp.nasdaqtrader.com" '''
    ftp = ftplib.FTP("ftp.nasdaqtrader.com")
    ftp.login()
    ftp.cwd("SymbolDirectory")
    
    r = io.BytesIO()
    ftp.retrbinary('RETR otherlisted.txt', r.write)
    
    info = r.getvalue().decode()
    splits = info.split("|")
    
    tickers = [x for x in splits if "N\r\n" in x]
    tickers = [x.strip("N\r\n") for x in tickers]
    tickers = [x.split("\r\n") for x in tickers]
    tickers = [sublist for outerlist in tickers for sublist in outerlist]
    
    ftp.close()    

    return tickers

def tickers_AEX(): #AEX
    '''Downloads list of tickers currently listed in the S&P 500 '''
    # get list of all S&P 500 stocks
    sp500 = pd.read_html("https://nl.wikipedia.org/wiki/AEX")[0]
    sp_tickers = sorted(sp500.Symbol.tolist())
    
    return sp_tickers

import os
os.chdir( 'C:/Users/Jesse/OneDrive/Bureaublad laptop Jesse/Beleggen/data/Excel_files_stocks')

sp500 =tickers_sp500()
sp500= pd.DataFrame(sp500,columns = ['ticker'])
sp500['index_ticker'] = 'S&P500'
sp500['comment'] = 'Import all stocks in S&P500 on '+ str(datetime.datetime.now())
sp500 = sp500.set_index('ticker')
sp500.to_csv('stocks_sp500.csv')

dow_jones =tickers_dow()
dow_jones= pd.DataFrame(dow_jones,columns = ['ticker'])
dow_jones['index_ticker'] = 'Dow Jones'
dow_jones['comment'] = 'Import all stocks in Dow Jones on '+ str(datetime.datetime.now())
dow_jones = dow_jones.set_index('ticker')
dow_jones.to_csv('stocks_dow_jones.csv')

nasdaq =tickers_nasdaq()
nasdaq= pd.DataFrame(nasdaq,columns = ['ticker'])
nasdaq['index_ticker'] = 'Nasdaq'
nasdaq['comment'] = 'Import all stocks in Nasdaq on '+ str(datetime.datetime.now())
nasdaq = nasdaq.set_index('ticker')
nasdaq.to_csv('stocks_nasdaq.csv')

# AEX By hand https://nl.wikipedia.org/wiki/AEX
# DAX By hand https://en.wikipedia.org/wiki/DAX
# Nikkei 220 by hand https://topforeignstocks.com/indices/the-components-of-the-nikkei-225-index/
# ftse100 by hand https://en.wikipedia.org/wiki/FTSE_100_Index
# AMX https://nl.wikipedia.org/wiki/AMX_Index
#CAC https://tradingeconomics.com/france/stock-market


#Merge all files in directory:
t1 = pd.read_csv("stocks_aex.csv",encoding = 'unicode_escape')
t2 = pd.read_csv("stocks_amx.csv",encoding = 'unicode_escape')
t3 = pd.read_csv("stocks_bel20.csv",encoding = 'unicode_escape')
t4 = pd.read_csv("stocks_dax.csv",encoding = 'unicode_escape')
t5 = pd.read_csv("stocks_dow_jones.csv",encoding = 'unicode_escape')
t6 = pd.read_csv("stocks_ftse100.csv",encoding = 'unicode_escape')
t7 = pd.read_csv("stocks_nasdaq_largest.csv",encoding = 'unicode_escape')
t8 = pd.read_csv("stocks_nikkei225.csv",encoding = 'unicode_escape')
t9 = pd.read_csv("stocks_sp500.csv",encoding = 'unicode_escape')
t10 = pd.read_csv("stocks.csv",encoding = 'unicode_escape')
t11 = pd.read_csv("stocks_cac.csv",encoding = 'unicode_escape')

final_df = pd.concat([t1, t2], ignore_index=True)
final_df = pd.concat([final_df, t3], axis=0)
final_df = pd.concat([final_df, t4], ignore_index=True)
final_df = pd.concat([final_df, t5], ignore_index=True)
final_df = pd.concat([final_df, t6], ignore_index=True)
final_df = pd.concat([final_df, t7], ignore_index=True)
final_df = pd.concat([final_df, t8], ignore_index=True)
final_df = pd.concat([final_df, t9], ignore_index=True)
final_df = pd.concat([final_df, t10], ignore_index=True)
final_df = pd.concat([final_df, t11], ignore_index=True)

final_df.set_index('ticker').to_csv('all_stocks.csv')
