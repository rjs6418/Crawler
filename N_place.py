import requests
from bs4 import BeautifulSoup
import time

def np_info(nps):
  for np in nps:
    try:
      search_url = f"https://pcmap.place.naver.com/place/list?query={np}"
      res_search = requests.get(search_url)
      html_search = res_search.content.decode('utf-8','replace')

      soup = BeautifulSoup(html_search, 'html.parser')
      low=soup.select("body.place_on_pcmap > script")[2].text.split("\n")[3].strip()
      a=low.find('Summary')
      b=low[a:].find('"')
      np_code = int(low[a+8:a+b])

      info_url = f"https://pcmap.place.naver.com/accommodation/{np_code}/home?businessCategory=camping"
      res_info = requests.get(info_url)
      html_info = res_info.content.decode('utf-8','replace')
      print(np_code)
      print(html_info)
    except:
      pass