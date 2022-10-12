import requests
from bs4 import BeautifulSoup

# S&P500 Symbol list 수집
def get_SnP500_list():
    SnP500_list_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    SnP500_list_html_request = requests.get(SnP500_list_url)
    SnP500_list_html = SnP500_list_html_request.content.decode('utf-8','replace')
    soup = BeautifulSoup(SnP500_list_html, 'html.parser')
    table = soup.select_one('table > tbody').select('tr')
    return [element.text.strip().split('\n')[0] for element in table[1:]]