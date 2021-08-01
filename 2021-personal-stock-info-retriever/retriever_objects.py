
import yfinance as yf

class StockInfoRetriever():
    def __init__(self):
        # general stock info
        self.market_cap = None
        self.industry = None
        self.sector = None
        # financial health related metrics
        self.quick_ratio = None
        self.current_ratio = None
        # valuation based metrics
        self.trailing_pe = None
        self.forward_pe = None
        self.eps = None
        self.div_yield = None
        self.enterprise_to_ebitda = None
        self.enterprise_to_sales = None
        self.peg_ratio = None
        # growth related metrics
        self.forward_eps = None

    def set_market_cap(self, stock_info, debug):
        if type(self.market_cap) != type(None):
            return
        try:
            self.market_cap = stock_info['marketCap']
            if debug:
                print("Market cap succesfully set to: {}".format(self.market_cap))
        except Exception as e:
            if debug:
                print(e)
            return

    def set_industry(self, stock_info, debug):
        if type(self.industry) != type(None):
            return
        try:
            self.industry = stock_info['industry']
            if debug:
                print("Industry succesfully set to: {}".format(self.industry))
        except Exception as e:
            if debug:
                print(e)
            return

    def set_sector(self, stock_info, debug):
        if type(self.sector) != type(None):
            return
        try:
            self.sector = stock_info['sector']
            if debug:
                print("Sector succesfully set to: {}".format(self.sector))
        except Exception as e:
            if debug:
                print(e)
            return

    def set_quick_ratio(self, stock_info, debug):
        if type(self.quick_ratio) != type(None):
            return
        try:
            self.quick_ratio = stock_info['quickRatio']
            if debug:
                print("Quick ratio succesfully set to: {}".format(self.quick_ratio))
        except Exception as e:
            if debug:
                print(e)
            return

    def set_current_ratio(self, stock_info, debug):
        if type(self.current_ratio) != type(None):
            return
        try:
            self.current_ratio = stock_info['currentRatio']
            if debug:
                print("Current ratio succesfully set to: {}".format(
                    self.current_ratio))
        except Exception as e:
            if debug:
                print(e)
            return

    def set_trailing_pe(self, stock_info, debug):
        if type(self.trailing_pe) != type(None):
            return
        try:
            self.trailing_pe = round(stock_info['trailingPE'], 2)
            if debug:
                print("Trailing PE succesfully set to: {}".format(self.trailing_pe))
        except Exception as e:
            if debug:
                print(e)
            return

    def set_forward_pe(self, stock_info, debug):
        if type(self.forward_pe) != type(None):
            return
        try:
            self.forward_pe = round(stock_info['forwardPE'], 2)
            if debug:
                print("Forward PE succesfully set to: {}".format(self.forward_pe))
        except Exception as e:
            if debug:
                print(e)
            return

    def set_eps(self, stock_info, debug):
        if type(self.eps) != type(None):
            return
        try:
            self.eps = round(stock_info['trailingEps'], 2)
            if debug:
                print("Earnings Per Share (EPS) succesfully set to: {}".format(self.eps))
        except Exception as e:
            if debug:
                print(e)
            return

    def set_div_yield(self, stock_info, debug):
        if type(self.div_yield) != type(None):
            return
        try:
            self.div_yield = stock_info['dividendYield']
            if debug:
                print("Dividend Yield succesfully set to: {}".format(self.div_yield))
        except Exception as e:
            if debug:
                print(e)
            return

    def set_enterprise_to_ebitda(self, stock_info, debug):
        if type(self.enterprise_to_ebitda) != type(None):
            return
        try:
            self.enterprise_to_ebitda = stock_info['enterpriseToEbitda']
            if debug:
                print("Enterprise to EBITDA succesfully set to: {}".format(
                    self.enterprise_to_ebitda))
        except Exception as e:
            if debug:
                print(e)
            return

    def set_enterprise_to_sales(self, stock_info, debug):
        if type(self.enterprise_to_sales) != type(None):
            return
        try:
            self.enterprise_to_sales = stock_info['enterpriseToRevenue']
            if debug:
                print("Enterprise to sales succesfully set to: {}".format(
                    self.enterprise_to_sales))
        except Exception as e:
            if debug:
                print(e)
            return

    def set_peg_ratio(self, stock_info, debug):
        if type(self.peg_ratio) != type(None):
            return
        try:
            self.peg_ratio = stock_info['pegRatio']
            if debug:
                print("PEG ratio succesfully set to: {}".format(self.peg_ratio))
        except Exception as e:
            if debug:
                print(e)
            return

    def set_forward_eps(self, stock_info, debug):
        if type(self.forward_eps) != type(None):
            return
        try:
            self.forward_eps = stock_info['forwardEps']
            if debug:
                print("Forward EPS succesfully set to: {}".format(self.forward_eps))
        except Exception as e:
            if debug:
                print(e)
            return

    def return_stock_info(self):
        return {
            "market_cap": self.market_cap,
            "industry": self.industry,
            "sector": self.sector,
            "quick_ratio": self.quick_ratio,
            "current_ratio": self.current_ratio,
            "trailing_pe": self.trailing_pe,
            "forward_pe": self.forward_pe,
            "eps": self.eps,
            "div_yield": self.div_yield,
            "enterprise_to_ebitda": self.enterprise_to_ebitda,
            "enterprise_to_sales": self.enterprise_to_sales,
            "peg_ratio": self.peg_ratio,
            "forward_eps": self.forward_eps
        }

    def run(self, ticker, debug=False):
        # Call yf API and retrieve all available metrics.
        try:
            ticker = yf.Ticker(ticker)
            stock_info = ticker.info
        except Exception as e:
            if debug:
                print(e)
                print("We couldn't retrieve any info for {}!".format(ticker))
            return

        self.set_market_cap(stock_info, debug)
        self.set_industry(stock_info, debug)
        self.set_sector(stock_info, debug)
        self.set_quick_ratio(stock_info, debug)
        self.set_current_ratio(stock_info, debug)
        self.set_trailing_pe(stock_info, debug)
        self.set_forward_pe(stock_info, debug)
        self.set_eps(stock_info, debug)
        self.set_div_yield(stock_info, debug)
        self.set_enterprise_to_ebitda(stock_info, debug)
        self.set_enterprise_to_sales(stock_info, debug)
        self.set_peg_ratio(stock_info, debug)
        self.set_forward_eps(stock_info, debug)

        if debug:
            print(self.return_stock_info())
