# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 17:11:41 2020

@author: Jesse
"""

import os
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import datetime
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels import regression
import yahoo_fin.stock_info as yf
import yfinance 
from yahoofinancials import YahooFinancials

from mysql_connector import MySQL_connector
from File_Logging import FileLogging

current_working_directory = os.getcwd()
file_logging = FileLogging(directory = current_working_directory + '\\Logging\\')

class Model_Calculation_Object(MySQL_connector):
    """
    Includes all steps to get important parameters for DDM or DCF analysis, such as: 
        - Yearly dividends
        - expected dividend growth
        - WACC (to be added) 
    
    and also semi important parameters such as: 
        - Current stock price
        - Country in which stock is located
        - Continent in which stock is located (for risk free rates)
        
    Uses:
        - Local MySQL database by inherited MySQL_connector class.
        - Several yahoo finance API's.
    """
    def __init__(self, ticker,print_messages = False):
        super().__init__()
        #MySQL_connector.__init__(self)
        self.print_messages = print_messages
        self.ticker = ticker
        self.intrinsic_value = None

    def get_pe_ratio(self,stats_data,correction_term = 1):
        """
        Adjust correction term if we except an overall market collaps in PE ratios .
        e.g. the pe ratio of the market is 25, but 15 is average, collapse of 15/25 might be excepted in the near future.
        """       
        try:
            self.pe_ratio = float(stats_data[stats_data['attribute'] == 'Forward P/E 1']['value'].iloc[0]) * correction_term
        except Exception as e:
            try:
                self.pe_ratio = float(stats_data[stats_data['attribute'] == 'Trailing P/E']['value'].iloc[0]) *correction_term
                self.forward_pe_used = False
                print('Error getting forward pe ratio in get_pe_ratio: ' + str(e))
            except IndexError as e:
                if self.print_messages:
                    print('Error, ticker does not exist: {0}'.format(e))
                file_logging.logger.info('Error, ticker does not exist: {0}'.format(e)) 
                self.pe_ratio = None
            
    def get_eps_ttm(self, stats_data):
        try:
            self.eps_ttm = float(stats_data[stats_data['attribute'] == 'Diluted EPS (ttm)']['value'].iloc[0])
        except Exception as e:
            if self.print_messages:
                print('Error getting EPS ttm in get_eps_ttm: ' + str(e))
            file_logging.logger.info('Error getting EPS ttm in get_eps_ttm: ' + str(e))

            self.eps_ttm = None
    
    def get_last_table_date_CF(self):       
        query = "SELECT max(date) as date from investing.cashflow where ticker = '{}';".format(self.ticker) 
        
        max_date = self.execute_select_query(query=query)['date'].iloc[0]
        
        return max_date 
        
    def get_last_table_date_stats(self):       
        query = "SELECT max(date) as date from investing.stats where ticker = '{}';".format(self.ticker) 
        
        max_date = self.execute_select_query(query=query)['date'].iloc[0]
     
        return max_date
    
    def get_last_table_date_analysts(self):       
        query = "SELECT max(date) as date from investing.analysts_estimates where ticker = '{}';".format(self.ticker) 
        
        max_date = self.execute_select_query(query=query)['date'].iloc[0]

        return max_date
    
    def get_ticker_data(self):
        max_date = self.get_last_table_date_stats()
        
        query = "select * from investing.stats where date = '{}' AND ticker = '{}';".format(max_date,self.ticker)
        
        stats_data = self.execute_select_query(query=query)
        
        return stats_data
            
    def get_stock_price(self):
        try:
            data = yf.get_data(self.ticker)
            self.stock_price =round(data.iloc[len(data)-1]['close'],2)
        except KeyError:
            self.stock_price = None

    
    def get_ticker_country(self):
        query = "SELECT ticker,country FROM investing.company where ticker = '{}' group by ticker;".format(self.ticker)
        country = self.execute_select_query(query = query)['country'].iloc[0]
        file_logging.logger.info('get_ticker_country done. get_ticker_country = {0}'.format(country))

        return country
    
    def get_ticker_continent(self):
        country = self.get_ticker_country()
        query = "SELECT t1.code as continent_code,t1.name as continent_name,t2.name as country_name FROM investing.continents t1 INNER JOIN investing.countries t2 ON t1.code = t2.continent_code WHERE t2.name like '{}';".format(country)
        continent =  country = self.execute_select_query(query = query)['continent_code'].iloc[0]
        file_logging.logger.info('get_ticker_continent done. get_ticker_continent = {0}'.format(continent))

        return continent
    
    def get_risk_free_rate(self):
        try:
            continent = self.get_ticker_continent()
            query = "SELECT max(date) AS 'most_recent_date',continent,rate FROM investing.risk_free_rates where continent = '{}' group by continent;".format(continent)
            risk_free_rate = float(self.execute_select_query(query = query)['rate'].iloc[0])
            file_logging.logger.debug('risk_free_rate done. risk_free_rate = {0}'.format(risk_free_rate))

            if self.print_messages:
                print('risk_free_rate done. risk_free_rate = {0}'.format(risk_free_rate))
        except IndexError:
            file_logging.logger.error('Unknown stock ticker {0} in get_risk_free_rate.'.format(self.ticker))

            risk_free_rate = None
        except Exception as e:
            file_logging.logger.error('Error in get_risk_free_rate: {0}'.format(str(e)))
            if self.print_messages:
                print('Unknown error in get_risk_free_rate: ' + e)
            risk_free_rate = None
        return float(risk_free_rate)
    
    def get_yearly_dividends(self):
        current_year = int(datetime.datetime.now().year)
        current_month = int(datetime.datetime.now().month)
        stock = yfinance.Ticker(self.ticker)
        
        # get stock info       
        dividends = stock.history(period="max")['Dividends'].resample('Y').sum().to_frame()
        
        #skip first years if they started paying dividend later on
        i = 0
        for div in dividends['Dividends']:
            if div == 0:
                dividends = dividends.drop(dividends.index[i])
                i+=1
            if div !=0:
                break
        # dividends in first quarter is not enough to estimate dividends this year
        # over we are half a year through, we expect double those dividends at the end of the year.
        
        if current_month <= 6:
            dividends = dividends[dividends.index.year != current_year]
        elif current_month >=7  and current_month <= 9:
            dividends[len(dividends)-1] = dividends[len(dividends)-1] * 4/2
        elif current_month >=10  and current_month <= 12:
            dividends[len(dividends)-1] = dividends[len(dividends)+1] * 4/3
        dividends = dividends.assign(year = [i for i in range(1,len(dividends.index)+1)])
        
        return float(dividends)

    def estimate_future_dividend_growth(self,dividends):
        #Use linear regression to estimate dividends next year based on dividends on previous years
        #Assumes linear growth !
        X = np.array(dividends['year']).reshape(-1, 1)
        y = np.array(dividends['Dividends'])
        reg = LinearRegression().fit(X, y)
        file_logging.logger.info('R2 score for dividend model: {} '.format(reg.score(X, y)))
        #X_pred = np.array(X[len(X)-1] + 1).reshape(-1,1)
        #prediction = reg.predict(np.array(X_pred))
        return float(reg.coef_[0])
    
    def get_yearly_growth_amount(self):
        # If payout ratio is already high, dividends are less likely to be raised in the future.
        # If dividend yield is unreasonably high (above 7% to 12%) dividends are probably stable.
        try:
            stats = yf.get_stats(self.ticker) # https://finance.yahoo.com/quote/NFLX/key-statistics?p=NFLX
            payout_ratio = float(stats[stats['Attribute'] == 'Payout Ratio 4']['Value'].item().replace('%','')) / 100
            dividend_yield = float(stats[stats['Attribute'] =='Trailing Annual Dividend Yield 3']['Value'].item().replace('%','')) /100

            dividends = self.get_yearly_dividends()
                     
            self.yearly_growth_amount = self.estimate_future_dividend_growth(dividends)
            if payout_ratio > 0.6 and self.yearly_growth_amount > 0:
                self.yearly_growth_amount =0
                file_logging.logger.info('High payout ratio, assume not room for future raising of dividends {0}'.format(self.ticker))

            if dividend_yield > 0.12:
                self.yearly_growth_amount = 0
                file_logging.logger.info('Unreasoble dividend rates, assume not growth in future for {0}'.format(self.ticker))

                
        except Exception as e:
            file_logging.logger.error('Error in get_yearly_growth_amount: {0}'.format(str(e)))
            if self.print_messages:
                print('Unknown error in get_yearly_growth_amount: ' + str(e))
            self.get_yearly_growth_amount = None
        
    def get_expected_growth_rate(self):
        #The percentage at which we expect the dividends to grow based on the previous 2 years.
        #get_yearly_growth_amount seems more reasonable as this models the dividends linearly
        #based on all yearly historic dividends. 
        try:
            sensible_years = [str(i) for i in range(2010,2040)]
            sensible_years = str(sensible_years).replace('[','(').replace(']',')')
            query = "SELECT * FROM investing.cashflow where ticker = '{}' AND attribute like '%dividend%' AND period in {}; ".format(self.ticker,sensible_years)
            balance_sheet_df = self.execute_select_query(query = query)
            
            dividends = balance_sheet_df['value'].to_list()
            no_dividends_paid = 0
            for element in dividends:
                if element == '-':
                    no_dividends_paid +=1
            if float(no_dividends_paid) / float(len(dividends)) > 0.5:
                self.expected_growth_rate = None
                return
            
            dividend_growth = [ (float(a1) / float(a2))-1 for a1, a2 in zip(dividends[1:], dividends)]
            mean_growth = np.mean(dividend_growth)
            self.expected_growth_rate = float(mean_growth)
            
            file_logging.logger.info('get_expected_growth_rate done. expected_growth_rate = {0}'.format(self.expected_growth_rate))
        except ZeroDivisionError:
            file_logging.logger.error('Unknown stock ticker {0} in get_expected_growth_rate.'.format(self.ticker))
            if self.print_messages:
                print('Unknown stock ticker {0} in get_expected_growth_rate.'.format(self.ticker))
            self.expected_growth_rate = None
        except Exception as e:
            file_logging.logger.error('Error in get_expected_growth_rate: {0}'.format(str(e)))
            if self.print_messages:
                print('Error in get_expected_growth_rate: {0}'.format(str(e)))
            self.expected_growth_rate = None
            
    def get_current_annual_dividend(self,ticker):
        yahoo_financials = YahooFinancials(self.ticker)
        try:
            self.current_annual_dividend = float(yahoo_financials.get_dividend_rate())
        except Exception as e:
            file_logging.logger.error('Error in get_current_annual_dividend: ' + str(e))

            if self.print_messages:
                print('Error in get_current_annual_dividend: ' + str(e))
            self.current_annual_dividend = None
            
    def get_estimated_market_return(self):
        try:
            continent = self.get_ticker_continent()
            query = "SELECT max(date) AS 'most_recent_date',continent,rate FROM investing.expected_market_returns where continent = '{}' group by continent;".format(continent)
            estimated_market_return = float(self.execute_select_query(query = query)['rate'].iloc[0])
            file_logging.logger.debug('get_estimated_market_return done. estimated_market_return = {0}'.format(estimated_market_return))
            
            if self.print_messages:
                print('get_estimated_market_return done. estimated_market_return = {0}'.format(estimated_market_return))        
        except IndexError:
            file_logging.logger.error('Unknown stock ticker {0} in get_estimated_market_return.'.format(self.ticker))
            
            if self.print_messages:
                print('Unknown stock ticker {0} in get_estimated_market_return.'.format(self.ticker))
            estimated_market_return = None
        except Exception as e:
            file_logging.logger.error('Error in get_estimated_market_return: {0}'.format(str(e)))
            
            if self.print_messages:
                print('Error in get_estimated_market_return: ' + str(e))
            estimated_market_return = None
        return float(estimated_market_return)
    
    def get_beta(self):
        try:
            continent = self.get_ticker_continent()
            if continent == 'EU':
                benchmark_ticker= '^GDAXI'
            elif continent == 'NA':
                benchmark_ticker= '^GSPC'
            elif continent == 'AS':
                benchmark_ticker= '000001.SS'
            else:
                print('Unsupported continent!')
            yfinance.pdr_override()
            
            start_date=str(datetime.datetime.now().date() + datetime.timedelta(days = -3650))
            end_date = str(datetime.datetime.now().date())
            
            ticker_data = pdr.get_data_yahoo(self.ticker,start = start_date,end = end_date,interval = '1wk').Close.pct_change()[1:-1]
           # ticker_data = ticker_data[ticker_data !=0]
       
            benchmark_data = pdr.get_data_yahoo(benchmark_ticker,start = start_date,end = end_date,interval = '1wk').Close.pct_change()[1:-1]
            
            ticker_data = pd.merge(ticker_data,benchmark_data,how='inner',left_index=True,right_index=True).groupby(level=0).max()['Close_x'].values
            benchmark_data = benchmark_data.values[0:len(ticker_data)]
            #x: market, y: ticker        
            benchmark_data = sm.add_constant(benchmark_data)
            model = regression.linear_model.OLS(ticker_data,benchmark_data).fit()
            benchmark_data = benchmark_data[:,1]
            
            beta = float(model.params[1])
            
            file_logging.logger.debug('get_beta done. beta = {0}'.format(beta))
            if self.print_messages:
                print('get_beta done. beta = {0}'.format(beta))
        except IndexError:
            file_logging.logger.error('Unknown stock ticker {0} in get_beta.'.format(self.ticker))
            if self.print_messages:
                print('Error: Unknown stock ticker.')
            beta = None
        except Exception as e:
            file_logging.logger.error('Error in get_beta: {0}'.format(str(e)))
            if self.print_messages:
                print('Unknown error in get_beta: ' + str(e))

        return float(beta)
    def get_simple_discount_rate(self):
        """
        CAPM (https://www.investopedia.com/terms/c/capm.asp).
        Formula:
        Discount_rate = beta * estimated market return + risk free rate
        """
        risk_free_rate = self.get_risk_free_rate()
        if risk_free_rate == None:
            self.discount_rate = None
            return
        estimated_market_return=self.get_estimated_market_return()
        if estimated_market_return == None:
             self.discount_rate = None
             return
        beta = self.get_beta()
        if beta == None:
             self.discount_rate = None
             return
        self.discount_rate = beta * estimated_market_return + risk_free_rate    
    
    def get_cash_level(self):
        last_date = self.get_last_table_date_stats()
        query = "SELECT * FROM investing.stats where attribute like 'Total cash (mrq)%' and ticker = '{}' and date = '{}';".format(self.ticker,last_date)
        data = self.execute_select_query(query=query)
        if len(data) > 0:
            if data['value'].iloc[0] != None:
                self.cash_level = float(data['value'].iloc[0])
            else:
                self.cash_level = 0
        else:
            file_logging.logger.info('Outstanding shares not found for company {}'.format(self.ticker))
            self.cash_level = None
            if self.print_messages == True:
                print('Outstanding shares not found for company {}'.format(self.ticker))

    def get_debt_level(self):
        last_date = self.get_last_table_date_stats()
        query = "SELECT * FROM investing.stats where attribute like 'Total debt (mrq)%' and ticker = '{}' and date = '{}';".format(self.ticker,last_date)
        data = self.execute_select_query(query=query)
        if len(data) > 0:
            if data['value'].iloc[0] != None:
                self.debt_level = float(data['value'].iloc[0])
            else:
                self.debt_level = 0
        else:
            file_logging.logger.info('Outstanding shares not found for company {}'.format(self.ticker))
            self.debt_level = None
            if self.print_messages == True:
                print('Outstanding shares not found for company {}'.format(self.ticker))
    
    def get_outstanding_shares(self):
        last_date = self.get_last_table_date_stats()
        query = "SELECT * FROM investing.stats where attribute like 'Shares Outstanding%' and ticker = '{}' and date = '{}';".format(self.ticker,last_date)
        data = self.execute_select_query(query=query)
        if len(data) > 0:
            self.nr_outstanding_shares = int(data['value'].iloc[0])
        else:
            file_logging.logger.info('Outstanding shares not found for company {}'.format(self.ticker))
            self.nr_outstanding_shares = None
            if self.print_messages == True:
                print('Outstanding shares not found for company {}'.format(self.ticker))
    
    def get_initial_cashflow(self):
        last_date = self.get_last_table_date_CF()
        query = "SELECT * FROM investing.cashflow where attribute like '%net income%' and period not like 'ttm' and date = '{}' and ticker = '{}';".format(last_date,self.ticker)
        data = self.execute_select_query(query=query)
        max_period = data['period'].max()
        if len(data) > 0:
            self.initial_cashflow = float(data[data['period'] == max_period]['value'].iloc[0])  * 1000
        else:
            file_logging.logger.info('Initial cashflow not found for company {}'.format(self.ticker))
            self.initial_cashflow = None
            if self.print_messages == True:
                print('Initial cashflow not found for company {}'.format(self.ticker))

    def get_five_year_growth_rate_estimates(self):
        last_date = self.get_last_table_date_analysts()
        query = "SELECT * FROM investing.analysts_estimates where attribute like 'Next 5 Year%' AND date = '{}' and ticker = '{}';".format(last_date,self.ticker)
        data = self.execute_select_query(query=query)
        if len(data) > 0:
            try:
                self.growth_rate = data[data['description'] == self.ticker]['value'].iloc[0]
                self.growth_rate = float(str(self.growth_rate).replace('%','')) / 100
            except ValueError:
                for value,benchmark in zip(data['value'].tolist(),data['description'].tolist()):
                    try:
                        if value != None:
                            self.growth_rate = float(value)
                            print('growth_rate (five years) of {} taken for company {}'.format(benchmark,self.ticker))
                    except Exception:
                        print('growth rate of benchmark {} couldnt be parsed to float!'.format(benchmark))
                        continue
        else:
            file_logging.logger.info('growth_rate (five years) not found for company {}'.format(self.ticker))
            self.growth_rate = None
            if self.print_messages == True:
                print('no growth_rate (five years) found for company {}'.format(self.ticker))