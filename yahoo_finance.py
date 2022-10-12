import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent

# S&P500 Symbol list 수집
def get_SnP500_list():
    SnP500_list_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    SnP500_list_html_request = requests.get(SnP500_list_url)
    SnP500_list_html = SnP500_list_html_request.content.decode('utf-8','replace')
    soup = BeautifulSoup(SnP500_list_html, 'html.parser')
    table = soup.select_one('table > tbody').select('tr')
    return [element.text.strip().split('\n')[0] for element in table[1:]]

def crawl_company_data(company_symbol):
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    search_company_uri = f"https://finance.yahoo.com/quote/{company_symbol}/history?p={company_symbol}"
    res_company_data= requests.get(search_company_uri, headers=headers)
    html_company_data = res_company_data.content.decode('utf-8','replace')
    soup = BeautifulSoup(html_company_data, 'html.parser')
    table = soup.select_one('table').select('tr')
    data_array = [list(map(lambda x : str(x)[6:-7], elements.select('span'))) for elements in table]
    return pd.DataFrame(data_array[1:-1], columns=data_array[0])
