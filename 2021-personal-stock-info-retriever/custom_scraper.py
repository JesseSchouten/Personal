"""
This is merely a test file to get some feeling for scraping of the raw yahoo.finance data. 
For yahoo finance specifically also exist usefull libraries in python, so this will probably not be used.
"""

import requests
import json

import pandas as pd
from bs4 import BeautifulSoup
import re


def get_headers():
    return {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


cookies = {
    'privacy-policy': '1,XXXXXXXXXXXXXXXXXXXXXX'
}

ticker = 'TSLA'
url = "https://finance.yahoo.com/quote/%s/analysis?p=%s" % (ticker, ticker)
response = requests.get(
    url, verify=False, headers=get_headers(), timeout=30, cookies=cookies)

soup = BeautifulSoup(response.text, 'html.parser')

pattern = re.compile(r'\s--\sData\s--\s')

script_data = soup.find('script', text=pattern).contents[0]

print(script_data)
