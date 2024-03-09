import requests
import pandas as pd
import json
import time

#https://github.com/RuchiTanmay/nselib

header = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36",
    "Sec-Fetch-User": "?1", "Accept": "*/*", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate",
    "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
    }




def nse_urlfetch(url):
    r_session = requests.session()
    nse_live = r_session.get("http://nseindia.com", headers=header)
    response = r_session.get(url, headers=header)
    return response


def get_price_volume_data(symbol: str, from_date: str, to_date: str):
    url = "https://www.nseindia.com/api/historical/securityArchives?"
    payload = f"from={from_date}&to={to_date}&symbol={symbol}&dataType=priceVolume&series=ALL&json=true"
    #print(url + payload)
    try:
        data_text = nse_urlfetch(url + payload).text
        with open('file.json', 'w') as f:
            f.write(data_text)
        f.close()
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    #data_text = open('file.json')
    resp = json.loads(data_text)
    return resp['data']


stock_names = ['NIFTYBEES', 'RELIANCE', 'BANKBEES', 'HDFCBANK', 'ICICIBANK', 'AXISBANK', 
'KOTAKBANK', 'HCLTECH', 'INFY', 'TCS', 'HDFCAMC', 'NAM_INDIA', 'HDFCLIFE', 'ICICIPRULI', 
'ICICIGI', 'BAJAJFINSV', 'BAJAJHLDNG', 'BAJFINANCE', 'HINDUNILVR', 'NESTLEIND', 'PGHH', 'PIDILITIND',
'COLPAL', 'DABUR', 'GILLETTE', 'ITC', 'TITAN', 'PAGEIND', 'BATAINDIA', 'HAVELLS', 'WHIRLPOOL',
'GLAXO', 'PFIZER', 'ABBOTINDIA', 'SANOFI', 'AKZOINDIA', 'BERGEPAINT', 'ASIANPAINT', 'BAJAJ_AUTO']

stock_names_next = ['UJJIVANSFB', '5PAISA', 'ANGELONE', 'ISEC', 'MOTILALOFS', 'MCX', 
'OFSS', 'TATAELXSI', 'TEAMLEASE', 'SIS', 'ASTRAZEN', 'BAYERCROP', 'ERIS', 'LALPATHLAB', 
'FINEORG', 'CAPLIPOINT', 'VINATIORGA', 'INDIGOPNTS', 'KANSAINER', '3MINDIA', 'GODREJCP', 'FINCABLES',
'DIXON', 'CERA', 'HONAUT', 'JCHAC', 'LUXIND', 'POLYCAB', 'RAJESHEXPO', 'RELAXO', 'SFL',
'VIPIND', 'TTKPRESTIG', 'BOSCHLTD', 'EICHERMOT', 'RADICO', 'SUNTV', 'MCDOWELL_N']

#Keep dates interval of 3 months max.
dateWindow = ['21-10-2023','20-12-2023']


def computeStocks(dat):
    count = 0
    lowest_price = float("inf")
    highest_price = float("-inf")
    for entry in dat:
        start_date = entry['CH_TIMESTAMP']
        high_price = entry['CH_TRADE_HIGH_PRICE']
        low_price = entry['CH_TRADE_LOW_PRICE']
        open_price = entry['CH_OPENING_PRICE']
        close_price = entry['CH_CLOSING_PRICE']
        if open_price < close_price:
            count = count+1
            if low_price < lowest_price:
                lowest_price = low_price
            if high_price > highest_price:
                highest_price = high_price

        else:
            #print(start_date, lowest_price,highest_price, int((highest_price*100)//lowest_price))
            if(highest_price >= 1.20*lowest_price):
                print("Buy found")
                print(start_date, lowest_price,highest_price, int((highest_price*100)//lowest_price))
            return count
    return count

for stk in stock_names+stock_names_next : 
    symbol = stk
    print("Running check for", stk)
    stock_data = []
    index = 0 
    while index < len(dateWindow)-1:
        #print("for data range",dateWindow[index], dateWindow[index+1])
        try:
            stock_data_part = get_price_volume_data(symbol=symbol, from_date=dateWindow[index], to_date=dateWindow[index+1])
            index = index + 1
        except:
            print("erro loading data, trying again")
            time.sleep(3)
        # for entry in stock_data:
        #     print(entry['CH_TIMESTAMP'], entry['CH_TRADE_HIGH_PRICE'] , entry['CH_TRADE_LOW_PRICE'],
        #         entry['CH_OPENING_PRICE'], entry['CH_CLOSING_PRICE'])
       
        stock_data = stock_data + stock_data_part




    i = 0
    while i < len(stock_data):
        start_date = stock_data[i]['CH_TIMESTAMP']
        open_price = stock_data[i]['CH_OPENING_PRICE']
        close_price = stock_data[i]['CH_CLOSING_PRICE']
        if open_price < close_price:
            i = i + computeStocks(stock_data[i:])
        else:
            i = i+1

