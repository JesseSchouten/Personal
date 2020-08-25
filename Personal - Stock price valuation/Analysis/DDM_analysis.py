# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 12:48:19 2020

@author: Jesse
"""

import os
import datetime

from model_calculations import Model_Calculation_Object
from File_Logging import FileLogging

current_working_directory = os.getcwd()
file_logging = FileLogging(directory = current_working_directory + '\\Logging\\')

class Discount_Dividend_Model(Model_Calculation_Object):
    """
    Multistage DDM with 'nr_years' of dividend at estimated growth rate 
    and 'perpetual_growth_rate'dividend growth rate in perpetuity.
    """
    def __init__(self,ticker,print_messages = False, is_test = False,params = None):
        super().__init__(ticker,print_messages)
        if params == None:
            self.nr_years_ahead = 5
            self.perpetual_growth_rate = 0.03
            self.margin_of_safety = 0.2
        else:
            self.nr_years_ahead = params['nr_years_ahead']
            self.perpetual_growth_rate = params['perpetual_growth_rate']
            self.margin_of_safety = params['margin_of_safety']
        #Model_Calculation_Object.__init__(self,ticker)
        self.stock_price = None
        
        self.yearly_growth_amount = None
        self.current_annual_dividend = None
        
        self.discount_rate = None #discount rate = beta * estimated market return + risk free rate
    
    def print_all_internal_variables(self):
        print('nr_years_ahead: {}'.format(self.nr_years_ahead))
        print('perpetual_growth_rate: {}'.format(self.perpetual_growth_rate))
        print('margin_of_safety: {}'.format(self.margin_of_safety))
        print('stock_price: {}'.format(self.stock_price))
        print('yearly_growth_amount: {}'.format(self.yearly_growth_amount))
        print('current_annual_dividend: {}'.format(self.current_annual_dividend))
        print('discount_rate: {}'.format(self.discount_rate))
    
    
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
        """
        Notation: D for dividends, PV for Present value.
        The intrinsic value is equal to the discounted terminal value 
        + the present value of all dividends in 'nr_years_ahead' years.
        """
  
        if self.discount_rate < self.perpetual_growth_rate:
            self.perpetual_growth_rate = 0.0
            
        D_PV_list = []
        D_list = []

        for year in range(1,self.nr_years_ahead+1):
            if year == 1:
                D0= self.current_annual_dividend
            else:
                D0 +=  self.yearly_growth_amount
            PV_div = D0 / (1+self.discount_rate)**year
            D_list.append(D0)
            D_PV_list.append(PV_div)
            
        #file_logging.logger.debug('discount rate = {0}'.format(str(discount_rate)))
        #file_logging.logger.debug('D_list = {0}'.format(str(D_list)))
        #file_logging.logger.debug('D_PV_list = {0}'.format(str(D_PV_list)))
        
        terminal_value = D_list[len(D_list) - 1]*(1+self.perpetual_growth_rate)/(self.discount_rate-self.perpetual_growth_rate)
        discounted_terminal_value = terminal_value/(1+self.discount_rate)**self.nr_years_ahead
        discounted_dividends_sum = sum(D_PV_list)
        
        self.intrinsic_value = discounted_terminal_value + discounted_dividends_sum
        
        #file_logging.logger.debug('terminal_value = {0}'.format(str(terminal_value)))
        #file_logging.logger.debug('discounted_terminal_value = {0}'.format(str(discounted_terminal_value)))
        #file_logging.logger.debug('Sum of present value of dividends = {0}'.format(discounted_dividends_sum))
        
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
                      ,'dcf_model':'DDM_model'
                      ,'growth_rate':self.yearly_growth_amount
                      ,'perpetual_growth_rate':self.perpetual_growth_rate
                      ,'discount_rate': self.discount_rate
                      ,'margin_of_safety':self.margin_of_safety
                      ,'years_ahead':self.nr_years_ahead
                      ,'estimated_price':self.intrinsic_value*(1-self.margin_of_safety)
                      ,'actual_price':self.stock_price
                      ,'is_undervalued': is_undervalued
                      ,'comments' : ''
                      ,'created':str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                      ,'updated':str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}
        
        
        self.insert_calculations(insert_row)
        if self.print_messages:
            print('terminal_value = {0}'.format(str(terminal_value)))
            print('D_list = {0}'.format(str(D_list)))
            print('D_PV_list = {0}'.format(str(D_PV_list)))
            
            print('discount rate = {0}'.format(str(self.discount_rate)))
            print('discounted_terminal_value = {0}'.format(str(discounted_terminal_value)))
            print('Sum of present value of dividends = {0}'.format(str(discounted_dividends_sum)))
            
            print('Intrinsic value is estimated to be: {}'.format(self.intrinsic_value))
            print('Pay at most {} ({} MOS)'.format(self.intrinsic_value*(1-self.margin_of_safety),self.margin_of_safety))
    
    def run(self):
        file_logging.logger.info('Starting: {0}'.format(self.ticker))
        if self.print_messages:
            print('Starting: {0}'.format(self.ticker))
            
        #if we can't get one of the metrics, quit the calculations.
        self.get_stock_price()
        if self.stock_price == None:
             return None
         
        self.get_yearly_growth_amount()
        if self.yearly_growth_amount == None:
            return None
        
        self.get_current_annual_dividend()
        if self.current_annual_dividend == None:
             return None
         
        self.get_simple_discount_rate()
        if self.discount_rate == None:
             return None

        
        params = {'risk_free_rate: {0}'.format(self.risk_free_rate)\
        ,'yearly_growth_amount: {0}'.format(self.yearly_growth_amount)\
        ,'annual dividend: {0}'.format(self.current_annual_dividend)\
        ,'estimated_market_return: {0}'.format(self.estimated_market_return)\
        ,'beta: {0}'.format(self.beta)}

        file_logging.logger.info('Starting intrinsic value calculation with parameters: {}'.format(params))
        if self.print_messages:
            print('Starting intrinsic value calculation with parameters: {}'.format(params))
            self.print_all_internal_variables()
        self.calculate() 
        
        return

#Discount_Dividend_Model('LHA.DE',True).run()
"""
To do:   
    Use WACC for discount rate.
    In the regression: do we take account for years with 0 dividend?
"""