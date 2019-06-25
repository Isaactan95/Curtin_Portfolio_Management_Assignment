from yahoofinancials import YahooFinancials as yf
import datetime, datedelta as dd, quandl
import pandas as pd

class utilites():

    def adjDate(var1):
        year, month, day = map(int, var1.split('-'))
        date1 = datetime.date(year, month, day) + dd.datedelta(days = 5)
        return date1

    def get_data1(ticker, Start, End):
        data = yf(ticker)
        stock = data.get_historical_price_data(Start, End, 'weekly')
        keys = list(stock.keys())
        
        stock1 = stock[keys[0]]
        list1 = list(stock1.keys())
        a1 = stock1[list1[5]]
        num_a1 = len(a1)
        i = 0
        price, date = list(), list()
        for i in range (num_a1):
            data1 = a1[i]
            data1_keys = list(data1.keys())
            p = data1[data1_keys[6]]
            d = data1[data1_keys[7]]
            price.append(p)
            date.append(d)
            i += 1
        return price, date

    def get_data(ticker, Start, End):
        data = yf(ticker)
        stock = data.get_historical_price_data(Start, End, 'weekly')
        keys = list(stock.keys())
        
        stock1 = stock[keys[0]]
        list1 = list(stock1.keys())
        a1 = stock1[list1[5]]
        num_a1 = len(a1)
        i = 0
        price, date = list(), list()
        for i in range (num_a1):
            data1 = a1[i]
            data1_keys = list(data1.keys())
            p = data1[data1_keys[6]]
            d = data1[data1_keys[7]]
            price.append(p)
            date.append(d)
            i += 1
        df = pd.DataFrame({"Date":date, "Close":price})
        df = df.set_index("Date", drop=False)
        del df["Date"]
    #    df = df.dropna()
        return df

    def getTB(start, end):
        quandl.ApiConfig.api_key = 'VPC45PqKzTo2Mnyvns1w'
        tb = quandl.get("FED/RIFSGFSM06_N_WF", start_date=start, end_date=end)
        return tb

    def enddate(date):
        u = datetime.datetime.strptime(date, "%Y-%m-%d")
        d = datetime.timedelta(weeks=27)
        t = str(u + d)
        return t[:10]

u = datetime.datetime.strptime('2018-02-24', "%Y-%m-%d")
d = datetime.timedelta(weeks=27)
t = str(u + d)
print(t[:10])