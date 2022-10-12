import requests
import pandas as pd
import itertools
from datetime import date
import time
from tqdm import tqdm

class NaKwET:
    
    def __init__(self, infod) :
        self.BASE_URL = infod['BASE_URL'] 
        self.API_KEY = infod['API_KEY']
        self.__SECRET_KEY = infod['SECRET_KEY']
        self.CUSTOMER_ID = infod['CUSTOMER_ID']
        self.method = infod['method']
        self.uri = infod['uri'] 
            
    #헤더 함수
    def __get_header(self):
        timestamp = str(round(time.time() * 1000))
        signature = Signature.generate(
            timestamp, self.method, self.uri, self.__SECRET_KEY)
        return {'Content-Type': 'application/json; charset=UTF-8',
                'X-Timestamp': timestamp, 'X-API-KEY': self.API_KEY,
                'X-Customer': str(self.CUSTOMER_ID), 'X-Signature': signature}
        
    #요청 url
    def __get_req_url(self, repkw):
        data_request_url = self.BASE_URL + self.uri + '?hintKeywords={}&showDetail=1'.format(repkw)
        return data_request_url

    #API requests
    def kw_vol(self, repkws, amt):
        data=[]
        z=0
        while repkws:
            resli = []
            for repkw in tqdm(repkws):
                time.sleep(0.17)
                resli += [requests.get(self.__get_req_url(repkw), headers=self.__get_header())]
            data += sum(map(lambda res: res.json()['keywordList'][:amt], [res for res in resli if str(res)=='<Response [200]>']), [])  
            repkws=list(itertools.compress(repkws, [0 if str(res)=='<Response [200]>' else 1 for res in resli]))
            if len(repkws)!=z: z=len(repkws); print(f'키워드 누락[\033[91m{len(repkws)}\033[0m]개')
            else: break
        df = pd.DataFrame(data).drop_duplicates(['relKeyword'], ignore_index = True)
        df.replace('< 10', int(0), inplace=True)
        df['date']=date.today()
        return  df

#네이버 광고 접근 정보
class AccInfo:

    def __init__(self,acce_info):
        self.acc_info=self.__conn_path[acce_info]

    __conn_path={
        'kunokw':{'BASE_URL' : 'https://api.naver.com', 
                  'API_KEY' : '', 
                  'SECRET_KEY' : '', 
                  'CUSTOMER_ID' : '', 
                  'method' : "GET", 
                  'uri' : '/keywordstool'}, 
        'kunokw_new':{}
        }

import hashlib
import hmac
import base64

class Signature:

    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"),
                        bytes(message, "utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())