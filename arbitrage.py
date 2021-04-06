import time
import urllib.parse
from typing import Optional, Dict, Any, List
from requests import Request, Session, Response
import hmac
from ciso8601 import parse_datetime
import json
import datetime
import requests

class FtxClient:
    _ENDPOINT = 'https://ftx.com/api/'

    def __init__(self, api_key=None, api_secret=None, subaccount_name=None) -> None:
        self._session = Session()
        self._api_key = api_key
        self._api_secret = api_secret
        self._subaccount_name = subaccount_name

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('GET', path, params=params)

    def _post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('POST', path, json=params)

    def _delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('DELETE', path, json=params)

    def _request(self, method: str, path: str, **kwargs) -> Any:
        request = Request(method, self._ENDPOINT + path, **kwargs)
        self._sign_request(request)
        response = self._session.send(request.prepare())
        return self._process_response(response)

    def _sign_request(self, request: Request) -> None:
        ts = int(time.time() * 1000)
        prepared = request.prepare()
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(self._api_secret.encode(), signature_payload, 'sha256').hexdigest()
        request.headers['FTX-KEY'] = self._api_key
        request.headers['FTX-SIGN'] = signature
        request.headers['FTX-TS'] = str(ts)
        if self._subaccount_name:
            request.headers['FTX-SUBACCOUNT'] = urllib.parse.quote(self._subaccount_name)

    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            if not data['success']:
                raise Exception(data['error'])
            return data['result']
        
    
    def get_balances(self)->List[dict]:
        return self._get('wallet/balances')

    def get_funding_payments(self,future:str) -> List[dict]:
        return self._get('funding_payments',{'future':future})

    def get_borrow_history(self)->List[dict]:
        return self._get('spot_margin/borrow_history',{'coin':'USD'})

    def get_account(self)->List[dict]:
        return self._get('account')


if __name__ == "__main__":
    LINE_API_KEY = 'LINE_NOTIFY_API_KEY'
    subaccount = FtxClient('API_KEY','API_SECRET','SUBACCOUNT_NAME')
    coinlist = ['BTC-PERP','ETH-PERP'] #套利幣種
    
    total = 0
    account = subaccount.get_account()
    balance = subaccount.get_balances()
    for coin in balance:
        total = total + coin['usdValue']
    
    cost_24h = 0
    borrow_history = subaccount.get_borrow_history()
    for i in range(24):
        cost_24h = cost_24h + borrow_history[i]['cost']

    payment_24h = 0
    for coin in coinlist:
        funding_payments = subaccount.get_funding_payments(future=coin)
        for i in range(24):
            payment_24h = payment_24h + funding_payments[i]['payment']
    
    '''
    print ('昨日收益：' + str(round((-payment_24h-cost_24h),2)) +
    '\n當日年化：' + str(round((-payment_24h*365/total*100),2)) + '%' +
    '\n帳戶餘額：' + str(round(total,2)) +
    '\n保證金：' + str(round((account['marginFraction']*100),2))+ '%' #lower than 3% will be liquidated
    )
    '''
    
    # Line Notify
    headers = {
        "Authorization": "Bearer " + LINE_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {"message": ' 期現套利'
    '\n昨日收益：' + str(round((-payment_24h-cost_24h),2)) +
    '\n當日年化：' + str(round((-payment_24h*365/total*100),2)) + '%' +
    '\n帳戶餘額：' + str(round(total,2)) +
    '\n保證金：' + str(round((account['marginFraction']*100),2))+ '%' }
    r = requests.post("https://notify-api.line.me/api/notify",
                        headers=headers, params=params)
