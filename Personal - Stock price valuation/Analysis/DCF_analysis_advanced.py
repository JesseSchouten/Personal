# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 12:48:03 2020

@author: Jesse
"""

import os
import datetime

from model_calculations import Model_Calculation_Object
from File_Logging import FileLogging

current_working_directory = os.getcwd()
file_logging = FileLogging(directory = current_working_directory + '\\Logging\\')

def get_terminal_value(FCF, g, d):
    """
    https://www.investopedia.com/terms/t/terminalvalue.asp:
    TV = (FCF * (1 + g)) / (d - g)
    where:
    FCF = Free cash flow for the last forecast period 
    g = Terminal growth rate    
    d = discount rate (which is usually the weighted average cost of capital)
    """
    
    return (FCF * (1+g)) / (d-g)
    

class Discount_CashFlow_Model_Advanced(Model_Calculation_Object):
    """
    .Based on free stock rover excel sheet.
    https://www.liberatedstocktrader.com/how-to-calculate-the-intrinsic-value-of-a-stock-buffet/
    
    if we choose period of 10 years:
        - growth rate % for first 5 years.
        - cool_down_growth_rate_factor * growth_rate % for second 5 years.
        - perpetual_growth_rate for eternity
    """
    def __init__(self,ticker,print_messages=False,is_test = False,params=None):
        super().__init__(ticker,print_messages)
        if params == None:
            self.perpetual_growth_rate = 0.02
            self.cool_down_growth_rate_factor = 0.3 # after x years, the initial growth rate slows down x%
            self.margin_of_safety = 0.5
            self.nr_years_ahead = 10
        else:
            None
        
        self.print_messages = print_messages
        self.test = is_test
        
        self.stock_price = None           
        self.initial_cashflow = None
        self.nr_outstanding_shares = None
        self.discount_rate = None #should be WACC.
        self.growth_rate = None #5 year estimates yahoo finance??
        self.debt_level = None
        self.cash_level = None
        
    def print_all_internal_variables(self):
        print('perpetual_growth_rate: {}'.format(self.perpetual_growth_rate))
        print('cool_down_growth_rate_factor: {}'.format(self.cool_down_growth_rate_factor))
        print('margin_of_safety: {}'.format(self.margin_of_safety))
        print('stock_price: {}'.format(self.stock_price))
        print('initial_cashflow: {}'.format(self.initial_cashflow))
        print('nr_outstanding_shares: {}'.format(self.nr_outstanding_shares))
        print('discount_rate: {}'.format(self.discount_rate))
        print('growth_rate: {}'.format(self.growth_rate))
        print('debt_level: {}'.format(self.debt_level))
        print('cash_level: {}'.format(self.cash_level))
    
    def insert_calculations(self,insert_data):
        insert_query = """
        INSERT INTO investing.undervalued_stocks
        (ticker,date,dcf_model,perpetual_growth_rate,growth_rate,discount_rate,margin_of_safety,years_ahead,estimated_price,actual_price,comments,created,updated)
        VALUES
        ('{}','{}','{}','{}',{},{},{},{},{},{},'{}','{}','{}')
        ON DUPLICATE KEY UPDATE
        `estimated_price` = estimated_price,
        `actual_price`=actual_price,
        `updated` =updated;""".format(insert_data['ticker'],insert_data['date'],insert_data['dcf_model'],insert_data['perpetual_growth_rate'],insert_data['growth_rate'],insert_data['discount_rate'],insert_data['margin_of_safety'],insert_data['years_ahead'],insert_data['estimated_price'],insert_data['actual_price'],insert_data['comments'],insert_data['created'],insert_data['updated'])
    
        insert_query = insert_query.replace('\n',' ')
        
        self.execute_defined_insert_query(insert_query)  

    def calculate(self):
        if self.test:
            self.initial_cashflow = 39240000000
            self.growth_rate = 0.111
            self.cool_down_growth_rate_factor = 0.04 / 0.111
            self.perpetual_growth_rate = 0.02
            self.discount_rate = 0.05
            self.nr_outstanding_shares = 7460000000
            self.debt_level = 86460000000
            self.margin_of_safety = 0.3
            self.stock_price = 137.39
            self.margin_of_safety = 0.3
        
        cashflow_list= []
        PV_list = []
        last_year_cf = self.initial_cashflow
        for year in range(1,self.nr_years_ahead + 1):
            if year <= self.nr_years_ahead / 2:   
                next_year_cf = (last_year_cf * (1 + self.growth_rate))
                cashflow_list.append(next_year_cf)
                PV = next_year_cf / (1+self.discount_rate)**year
                PV_list.append(PV)
                last_year_cf = next_year_cf
            elif year > self.nr_years_ahead / 2:
                next_year_cf = last_year_cf * (1+self.growth_rate* self.cool_down_growth_rate_factor)
                cashflow_list.append(next_year_cf)
                PV = next_year_cf / (1+self.discount_rate)**year
                PV_list.append(PV)
                last_year_cf = next_year_cf

            
        
        total_PV =sum(PV_list)
        terminal_value = get_terminal_value(PV_list[self.nr_years_ahead-1],self.perpetual_growth_rate,self.discount_rate)
        
        total_PV_of_cashflows = terminal_value + total_PV
        
        self.intrinsic_value = (total_PV_of_cashflows- self.debt_level) / self.nr_outstanding_shares

        file_logging.logger.info('Intrinsic value is estimated to be: {}'.format(self.intrinsic_value))
        file_logging.logger.info('Pay at most: {}  ({} MOS)'.format(self.intrinsic_value*self.margin_of_safety,self.margin_of_safety))

        is_undervalued = 0
        if self.intrinsic_value*(1-self.margin_of_safety) > self.stock_price:          
            file_logging.logger.info('stock {} is undervalued'.format(self.ticker))
            is_undervalued = 1
            if self.print_messages:
                print('stock {} is undervalued'.format(self.ticker)) 
            
        insert_row = {'ticker':self.ticker
                      ,'date':str(datetime.datetime.now().date())
                      ,'dcf_model':'Advanced DCF model'
                      ,'growth_rate':self.growth_rate
                      ,'perpetual_growth_rate':self.perpetual_growth_rate
                      ,'discount_rate': self.discount_rate
                      ,'margin_of_safety':self.margin_of_safety
                      ,'years_ahead':self.nr_years_ahead
                      ,'estimated_price':self.intrinsic_value*(1-self.margin_of_safety)
                      ,'actual_price':self.stock_price
                      ,'is_undervalued': is_undervalued
                      ,'comments' : 'cooling_down_growth_factor: {}'.format(self.cool_down_growth_rate_factor)
                      ,'created':str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                      ,'updated':str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}
        
        
        self.insert_calculations(insert_row)
        if self.print_messages:
            print('All PV values: {}'.format(PV_list))
            print('All cashflow values: {}'.format(cashflow_list))
            print('terminal value: {}'.format(terminal_value))  
            print('total PV: {}'.format(total_PV))
            print('Total of PV values: {}'.format(total_PV_of_cashflows))
            print('Debt level: {}'.format(self.debt_level))
            print('Cash level: {}'.format(self.cash_level))
    
            print('Intrinsic value is estimated to be: {}'.format(self.intrinsic_value))
            print('Pay at most {} ({} MOS)'.format(self.intrinsic_value*(1-self.margin_of_safety),self.margin_of_safety))

    def run(self):  
        if not self.test:            
            self.get_initial_cashflow()
            if self.initial_cashflow == None or self.initial_cashflow < 0:
                return None
            
            self.get_stock_price()
            if self.stock_price == None:
                return None
            
            self.get_outstanding_shares()
            if self.nr_outstanding_shares == None:
                return None
            
            self.get_debt_level()
            if self.debt_level == None:
                return None
            
            self.get_cash_level()
            if self.cash_level == None:
                return None 
            
            self.get_five_year_growth_rate_estimates()
            if self.growth_rate == None:
               # return None
               self.growth_rate = 0.0
               self.perpetual_growth_rate = 0.0
            
            self.get_simple_discount_rate()
            if self.discount_rate == None:
                return None
            
            if self.perpetual_growth_rate > self.discount_rate:
                print('self.perpetual_growth_rate > self.discount_rate')
                self.perpetual_growth_rate = 0
                #self.discount_rate = 0.08
            self.discount_rate = 0.0502
            params = {'stock_price: {0}'.format(self.stock_price)\
            ,'outstanding_shares: {0}'.format(self.nr_outstanding_shares)\
            ,'initial_cashflow: {0}'.format(self.initial_cashflow)\
            ,'debt_level: {0}'.format(self.debt_level)\
            ,'cash_level: {0}'.format(self.cash_level)\
            ,'growth_rate: {0}'.format(self.growth_rate)\
            ,'discount_rate: {0}'.format(self.discount_rate)}
                
            file_logging.logger.info('Starting intrinsic value calculation with parameters: {}'.format(params))
            if self.print_messages:
                print('Starting intrinsic value calculation with parameters: {}'.format(params))
                self.print_all_internal_variables()
                
        self.calculate()
  
Discount_CashFlow_Model_Advanced(ticker='V',print_messages = True).run()

