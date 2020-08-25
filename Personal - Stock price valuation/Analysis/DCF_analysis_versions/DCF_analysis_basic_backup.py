# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#os.chdir('C:/Users/Jesse/OneDrive/Bureaublad laptop Jesse/Beleggen/data')

import os
import argparse
from File_Logging import FileLogging
import datetime

import mysql_functions as MySQL_func
import yahoo_fin.stock_info  as yf

def getAllTickers():
    host_name = 'localhost'
    user = 'root'
    passwd = 'root'
    db_name = 'investing'
    mysql_conn = MySQL_func.connect_to_mysql_db(host_name,db_name,user,passwd)
    
    query = "SELECT ticker from investing.stats group by ticker;"
    
    tickers = MySQL_func.execute_select_query(mysql_conn,query=query)['ticker'].to_list()
    
    return tickers


def getLastTableDate(mysql_conn,ticker):
    
    query = "SELECT max(date) as date from investing.stats where ticker = '{}';".format(ticker) 
    
    max_date = MySQL_func.execute_select_query(mysql_conn,query=query)['date'].iloc[0]
    
    return max_date
    
def getTickerData(mysql_conn, ticker):
    max_date = getLastTableDate(mysql_conn,ticker)
    
    query = "select * from investing.stats where date = '{}' AND ticker = '{}';".format(max_date,ticker)
    
    stats_data = MySQL_func.execute_select_query(mysql_conn,query=query)
    
    return stats_data

def getStockPrice(ticker):
    data = yf.get_data(ticker)
    stock_price =round(data.iloc[len(data)-1]['close'],2)
    
    return stock_price

def insert_stock(mysql_conn,value):
    query = """
    INSERT INTO investing.undervalued_stocks
    (ticker,date,dcf_model,growth_rate,discount_rate,margin_of_safety,years_ahead,estimated_price,actual_price,created,updated)
    VALUES
    ('{}','{}','{}',{},{},{},{},{},{},'{}','{}')
    ON DUPLICATE KEY UPDATE
    `estimated_price` = estimated_price,
    `actual_price`=actual_price,
    `updated` =updated;""".format(value['ticker'],value['date'],value['dcf_model'],value['growth_rate'],value['discount_rate'],value['margin_of_safety'],value['years_ahead'],value['estimated_price'],value['actual_price'],value['created'],value['updated'])

    query = query.replace('\n',' ')

    mysql_conn_cursor = mysql_conn.cursor()
    
    mysql_conn_cursor.execute(query)
    
    mysql_conn.commit()
    
    mysql_conn_cursor.close()
    
    return
  
def DCF_basic(ticker,growth_rate,min_rate_of_return,margin_of_safety,years_ahead):
    """
    Basic DCF calculation based on Phil Towns rule #1 of investing.
    """
    
    global file_logging
    
    host_name = 'localhost'
    user = 'root'
    passwd = 'root'
    db_name = 'investing'
    forward_pe_used = True
    is_undervalued = 0
    try:
        mysql_conn = MySQL_func.connect_to_mysql_db(host_name,db_name,user,passwd)
        
        stats_data = getTickerData(mysql_conn, ticker)
        
        eps_ttm = float(stats_data[stats_data['attribute'] == 'Diluted EPS (ttm)']['value'].iloc[0])
            
        growth_rate = float(growth_rate)
        
        min_rate_of_return= float(min_rate_of_return)
        
        margin_of_safety = float(margin_of_safety)
        """
        #Always work with the lowest PE ratio availlable to be pessimistic.
        try:
            pe_ratio_forw = float(stats_data[stats_data['attribute'] == 'Forward P/E 1']['value'].iloc[0])
            pe_ratio_trail = float(stats_data[stats_data['attribute'] == 'Trailing P/E']['value'].iloc[0])
            if pe_ratio_forw > pe_ratio_trail:
                pe_ratio = pe_ratio_trail
            else:
                pe_ratio = pe_ratio_forw
                forward_pe_used = False
        except Exception:
            try:
                pe_ratio = float(stats_data[stats_data['attribute'] == 'Forward P/E 1']['value'].iloc[0])
            except Exception:
                pe_ratio = float(stats_data[stats_data['attribute'] == 'Trailing P/E']['value'].iloc[0])
                forward_pe_used = False
        """
        correction_term = 1 #correct the pe ratio's compared to the average of the market over the history
        
        try:
            pe_ratio = float(stats_data[stats_data['attribute'] == 'Forward P/E 1']['value'].iloc[0]) * correction_term
        except Exception:
            pe_ratio = float(stats_data[stats_data['attribute'] == 'Trailing P/E']['value'].iloc[0]) *correction_term
            forward_pe_used = False
                
        if pe_ratio < 0 or eps_ttm < 0:
            print(ticker + ' has negative PE ratio or EPS (trailing or forward), cancel calculations.')
            return
        
        stock_price = float(getStockPrice(ticker))
        
    except Exception as e:
        print(ticker + ' failed: ' +str(e))
        file_logging.logger.info(ticker + ' failed, error: ' +str(e))
        return
    expected_growth = eps_ttm
    for year in range(1,years_ahead):
        expected_growth =expected_growth *(1+growth_rate)
    
    expected_value_of_stock = expected_growth * pe_ratio
    for year in range(1,years_ahead):
        expected_value_of_stock = expected_value_of_stock / (1+min_rate_of_return)
    
    expected_value_of_stock_MOS = expected_value_of_stock*(1-margin_of_safety)
    
    print('{} - estimated price {}, actual price {}, forward pe used: {}'.format(ticker,expected_value_of_stock_MOS,stock_price,forward_pe_used))
    file_logging.logger.info('{} - estimated price {}, actual price {}, forward pe used: {}'.format(ticker,expected_value_of_stock_MOS,stock_price,forward_pe_used))
    if expected_value_of_stock_MOS > stock_price:
        print('stock {} is undervalued'.format(ticker)) 
        file_logging.logger.info('stock {} is undervalued'.format(ticker))
        is_undervalued = 1
        
    insert_row = {'ticker':ticker
                  ,'date':str(datetime.datetime.now().date())
                  ,'dcf_model':'Basic_DCF_model'
                  ,'growth_rate':growth_rate
                  ,'discount_rate':min_rate_of_return
                  ,'margin_of_safety':margin_of_safety
                  ,'years_ahead':years_ahead
                  ,'estimated_price':expected_value_of_stock_MOS
                  ,'actual_price':stock_price
                  ,'is_undervalued': is_undervalued
                  ,'created':str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                  ,'updated':str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}
    insert_stock(mysql_conn,insert_row)
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser("Research stock tickers by basic, adjusted DCF analysis")
    
    parser.add_argument(
        "--working_directory",
        default = 'C:/Users/Jesse/OneDrive/Bureaublad laptop Jesse/Beleggen/data/Analysis/',
        help="working directory of main script",
    )
    
    parser.add_argument(
        "--ticker",
        default = None,
        help="single ticker for calculations",
    )  
    
    parser.add_argument(
        "--growth_rate",
        default = 0.02,
        help="desired growth rate",
    )   
    
    parser.add_argument(
        "--min_rate_of_return",
        default = 0.15,
        help="desired rate of return",
    )   
        
    parser.add_argument(
        "--years_ahead",
        default = 5,
        help="desired years ahead to base forecast on",
    ) 
    
    parser.add_argument(
        "--margin_of_safety",
        default = 0.4,
        help="desired margin of safety, according to buffet, set to 20-50% based on your confidence in the specific stock.",
    )  
    
    parser.add_argument(
        "--test",
        default = False,
        help="Is this a test?",
    )   
    
    args = parser.parse_args()
    
    ticker = args.ticker
    
    working_directory = args.working_directory
    
    growth_rate = float(args.growth_rate)

    min_rate_of_return = float(args.min_rate_of_return)
    
    years_ahead = int(args.years_ahead)
    
    margin_of_safety = float(args.margin_of_safety)
    
    test = bool(args.test)
    
    file_logging = FileLogging(directory=working_directory)
    
    file_logging.logger.info('Starting basic DCF analysis:\n'\
                             'growth rate: ' + str(growth_rate) +'\n'+\
                             'min_rate_of_return: ' + str(min_rate_of_return) +'\n'+\
                             'years_ahead: ' + str(years_ahead) +'\n'+\
                             'margin_of_safety: ' + str(margin_of_safety) )

    if test:
        ticker = 'NFLX'
        DCF_basic(ticker,growth_rate,min_rate_of_return,margin_of_safety,years_ahead)
    elif ticker != None:
        DCF_basic(ticker,growth_rate,min_rate_of_return,margin_of_safety,years_ahead)
    else:
        tickers = getAllTickers()
        for ticker in tickers:
            DCF_basic(ticker,growth_rate,min_rate_of_return,margin_of_safety,years_ahead)
            
#DCF_basic('FB',0.10,min_rate_of_return,0,10)           
"""
Ideas:
    Adjust for corrected market: all PE ratios will go from 22.5 to 15 in the next 5 years. 
    (could take average of the two, or the mean, we should work with the mean P/E ratio over time, recession and non recession)
        Some companies will get hit more then other, if PE ratio is already low, they should suffer less
        Some sector will get hit more then other, sectors with a relatively low PE ratio should suffer less
    If analysts are positive, give a boost to the expected growth rate of the EPS, or take growth rate directly sometimes.
        If negative, increase margin of safety?
        Maybe check balance sheet for stability of EPS throughout the years? Increase margin of safety if not very stable. Decrease if stable.
    Maybe increase/decrease margin of safety based on other criteria's
        stability in revenue increase
        Number of debt, if it has debt, is it currently paying off debt?
        Current ratio
        P/E * P/B >22.5 satisfied (or give advantage if not satisfied)
        Does the compant buy back its shares
    Take account for economic cycles
        Suppose in the next years, we will have an average growth of 2%, 2 years of -10%, 3 years of + 13%(, variable growth rate)
    Which companies (from which sector, etc) are more sensitive to economic cycles?
        Punish severely in growth rate or margin of safety
    Maybe add dividends to cash flow 
        [NO, probably not a good idea, as the dividends are already part of the net profit]
        or: does a company give dividend? Yes, decrease margin of safety for each % of yield
        , maybe increase margin of safety for extreme dividends
        , payout ratio not too high, room for raising dividends
        , OR if debt is issued while dividends are issued.
        , Though, might be hard to determine in what sense dividends are paid in case of a recession.
        Probably best to research what a company does with its net income
            - reinvest? succesfully, or unsuccesfully?
            - pay dividends?
            - pay off debt? 
            - If is gets lost-> big warning!
    
    
Ideas for new algorithms:
    Divident growth model: https://www.investopedia.com/terms/g/gordongrowthmodel.asp     
       
    Terminal growth model
    
    Script to identify dividend growth companies
        Reasonable dividend yield (3-8%)
        Not too high payout ratio <50%
        
    Create a model that identifies all criteria for a 'solid' company according to buffet
        Stable growth of CF, low debt, solid balance sheet, 
"""