# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 17:26:57 2020

@author: Jesse
"""


import os
import sys
import argparse

from mysql_connector import MySQL_connector
from DDM_analysis import Discount_Dividend_Model
from DCF_analysis_advanced import Discount_CashFlow_Model_Advanced
from DCF_analysis_basic import Discount_CashFlow_Model_Basic
from File_Logging import FileLogging

def getAllTickers():
    mysql_conn = MySQL_connector()
    
    query = "SELECT ticker from investing.stats group by ticker;"
    
    tickers = mysql_conn.execute_select_query(query=query)['ticker'].to_list()
    
    return tickers

def main(ticker = None, run_DDM = False,run_advanced_DCF = False,run_basic_DCF = False,print_messages = False):
    if ticker == None:
        tickers = getAllTickers()
    else:
        tickers = [ticker]
        
    for ticker in tickers:
        if run_DDM:
            Discount_Dividend_Model(ticker=ticker,print_messages = print_messages).run()
        if run_advanced_DCF:
            Discount_CashFlow_Model_Advanced(ticker=ticker,print_messages = print_messages).run()
        if run_basic_DCF:
            Discount_CashFlow_Model_Basic(ticker=ticker,print_messages =print_messages).run()          

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Gets data from yahoo.finance")

    parser.add_argument(
        "--working_directory",
        default = 'C:/Users/Jesse/OneDrive/Bureaublad laptop Jesse/Beleggen/data/Analysis',
        help="working directory of main script",
    )
    
    parser.add_argument(
        "--ticker",
        default = False,
        help="Boolean whether daily statistics should be retrieved or not.",
    )
    
    parser.add_argument(
        "--run_DDM",
        default = False,
        help="Boolean whether to run the DDM model or not",
    )
        
    parser.add_argument(
        "--run_advanced_DCF",
        default = False,
        help="Boolean whether to run the advanced DCF model or not",
    )
            
    parser.add_argument(
        "--run_basic_DCF",
        default = False,
        help="Boolean whether to run the basic DCF model or not",
    )
                
    parser.add_argument(
        "--print_messages",
        default = False,
        help="Boolean whether to print messages or not.",
    )

    args = parser.parse_args()

    working_directory = args.working_directory
    
    ticker = args.ticker
    
    run_DDM = args.run_DDM
    run_advanced_DCF = args.run_advanced_DCF
    run_basic_DCF = args.run_basic_DCF
    
    print_messages = args.print_messages
    
    os.chdir(working_directory)
    
    #Global variables
    file_logging = FileLogging(directory=working_directory)

    main(ticker=ticker, run_DDM = run_DDM, run_advanced_DCF = run_advanced_DCF, run_basic_DCF = run_basic_DCF,print_messages=print_messages)

main('NFLX',True,True,True,True)   
"""
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
    
    if test:
        ticker = 'NFLX'
        DCF_basic(ticker,growth_rate,min_rate_of_return,margin_of_safety,years_ahead)
    elif ticker != None:
        DCF_basic(ticker,growth_rate,min_rate_of_return,margin_of_safety,years_ahead)
    else:
        tickers = getAllTickers()
        for ticker in tickers:
            DCF_basic(ticker,growth_rate,min_rate_of_return,margin_of_safety,years_ahead)

"""