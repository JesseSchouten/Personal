# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#os.chdir('C:/Users/Jesse/OneDrive/Bureaublad laptop Jesse/Beleggen/data')

import os
import argparse
import datetime
import yahoo_fin.stock_info  as yf

from model_calculations import Model_Calculation_Object
from File_Logging import FileLogging
import mysql_functions as MySQL_func
from mysql_connector import MySQL_connector

current_working_directory = os.getcwd()
os.chdir('C:/Users/Jesse/OneDrive/Bureaublad laptop Jesse/Beleggen/data/Analysis')
file_logging = FileLogging(directory = current_working_directory + '\\Logging\\')

class Discount_CashFlow_Model_Basic(Model_Calculation_Object):
    """
    Basic DCF calculation based on Phil Towns rule #1 of investing.
    """
    def __init__(self,ticker,print_messages = False,is_test=False,params=None):
        super().__init__(ticker,print_messages)
        if params == None:
            self.growth_rate = 0.02
            self.nr_years_ahead = 5
            self.margin_of_safety = 0.2
            self.forward_pe_used = True
            self.discount_rate = 0.15 #for this model the min desired rate of return.
        else:
            self.growth_rate = float(params['growth_rate'])
            self.nr_years_ahead = int(params['nr_years_ahead'])
            self.margin_of_safety = float(params['margin_of_safety'])
            self.forward_pe_used = params['forward_pe_used']
            self.discount_rate = float(params['discount_rate'] )
        self.print_messages = print_messages
        self.stock_price = None
            
        self.pe_ratio = None
        self.eps_ttm = None
    
    def print_all_internal_variables(self):
        print('growth_rate: {}'.format(self.growth_rate))
        print('nr_years_ahead: {}'.format(self.nr_years_ahead))
        print('margin_of_safety: {}'.format(self.margin_of_safety))
        print('forward_pe_used: {}'.format(self.forward_pe_used))
        print('discount_rate: {}'.format(self.discount_rate))
        print('stock_price: {}'.format(self.stock_price))
        print('pe_ratio: {}'.format(self.pe_ratio))
        print('eps_ttm: {}'.format(self.eps_ttm))
    
    
    def insert_calculations(self,insert_data):
        insert_query = """
        INSERT INTO investing.undervalued_stocks
        (ticker,date,dcf_model,growth_rate,discount_rate,margin_of_safety,years_ahead,estimated_price,actual_price,comments,created,updated)
        VALUES
        ('{}','{}','{}',{},{},{},{},{},{},'{}','{}','{}')
        ON DUPLICATE KEY UPDATE
        `estimated_price` = estimated_price,
        `actual_price`=actual_price,
        `updated` =updated;""".format(insert_data['ticker'],insert_data['date'],insert_data['dcf_model'],insert_data['growth_rate'],insert_data['discount_rate'],insert_data['margin_of_safety'],insert_data['years_ahead'],insert_data['estimated_price'],insert_data['actual_price'],insert_data['comments'],insert_data['created'],insert_data['updated'])
    
        insert_query = insert_query.replace('\n',' ')
        
        self.execute_defined_insert_query(insert_query)  
   
    def calculate(self):
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
        is_undervalued = 0
    
        expected_growth = self.eps_ttm
        for year in range(1,self.nr_years_ahead):
            expected_growth =expected_growth *(1+self.growth_rate)
        
        self.intrinsic_value = expected_growth * self.pe_ratio
        for year in range(1,self.nr_years_ahead):
            self.intrinsic_value = self.intrinsic_value / (1+self.discount_rate)
        if self.print_messages:
            print('{} - estimated price (with MOS) {}, actual price {}, forward pe used: {}'.format(self.ticker, self.intrinsic_value*(1-self.margin_of_safety),self.stock_price,self.forward_pe_used))
        file_logging.logger.info('{} - estimated price {}, actual price {}, forward pe used: {}'.format(self.ticker, self.intrinsic_value*(1-self.margin_of_safety),self.stock_price,self.forward_pe_used))
        if  self.intrinsic_value*(1-self.margin_of_safety) > self.stock_price:
            if self.print_messages:
                print('stock {} is undervalued'.format(self.ticker)) 
            file_logging.logger.info('stock {} is undervalued'.format(self.ticker))
            is_undervalued = 1
            
        insert_row = {'ticker':self.ticker
                      ,'date':str(datetime.datetime.now().date())
                      ,'dcf_model':'Basic_DCF_model'
                      ,'growth_rate':self.growth_rate
                      ,'discount_rate':self.discount_rate
                      ,'margin_of_safety':self.margin_of_safety
                      ,'years_ahead':self.nr_years_ahead
                      ,'estimated_price': self.intrinsic_value*(1-self.margin_of_safety)
                      ,'actual_price':self.stock_price
                      ,'is_undervalued': is_undervalued
                      ,'comments' : ''
                      ,'created':str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                      ,'updated':str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}
        self.insert_calculations(insert_row)
    
    def run(self):  
        stats_data = self.get_ticker_data()
        if len(stats_data) == 0:
            file_logging.logger.error('Script aborted at get_ticker_data: {0}'.format(self.ticker))
            if self.print_messages:
                print('Script aborted at getTickerData: {0}'.format(self.ticker))
            return None
        
        self.get_eps_ttm(stats_data)
        if self.get_eps_ttm == None:
            file_logging.logger.error('Script aborted at get_eps_ttm: {0}'.format(self.ticker))
            if self.print_messages:
                print('Script aborted at get_eps_ttm: {0}'.format(self.ticker))
            return None
        
        self.get_pe_ratio(stats_data)
        if self.pe_ratio == None:
            file_logging.logger.error('Script aborted at get_pe_ratio: {0}'.format(self.ticker))
            if self.print_messages:
                print('Script aborted at get_pe_ratio: {0}'.format(self.ticker))
            return None
        
        if self.pe_ratio < 0 or self.eps_ttm < 0:
            file_logging.logger.error(self.ticker + ' has negative PE ratio or EPS (trailing or forward), cancel calculations.')
            if self.print_messages:
                print(self.ticker + ' has negative PE ratio or EPS (trailing or forward), cancel calculations.')
            return None
        
        self.get_stock_price()
        if self.get_stock_price == None:
            file_logging.logger.error('Script aborted at get_stock_price: {0}'.format(self.ticker))
            if self.print_messages:
                print('Script aborted at get_stock_price: {0}'.format(self.ticker))
            return None
        params = {'eps_ttm: {0}'.format(self.eps_ttm)\
        ,'pe_ratio: {0}'.format(self.pe_ratio)\
        ,'stock_price: {0}'.format(self.stock_price)}
            
        file_logging.logger.info('Starting intrinsic value calculation with parameters: {}'.format(params))
        if self.print_messages:
            print('Starting intrinsic value calculation with parameters: {}'.format(params))
            self.print_all_internal_variables()
            
        self.calculate()
#Discount_CashFlow_Model_Basic('LHA.DE',True).run()      
Discount_CashFlow_Model_Basic('FB',True).run()   

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