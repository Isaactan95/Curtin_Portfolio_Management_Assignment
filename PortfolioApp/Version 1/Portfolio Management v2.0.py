# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 11:44:09 2018

@author: User
"""

from yahoofinancials import YahooFinancials as yf
import quandl
import pandas as pd
import numpy as np
from numpy import corrcoef
import math
from scipy import stats
import datetime
import sys
import time
import datedelta as dd

def adjDate(var1):
    year, month, day = map(int, var1.split('-'))
    date1 = datetime.date(year, month, day) + dd.datedelta(days = 5)
    return date1

quandl.ApiConfig.api_key = 'VPC45PqKzTo2Mnyvns1w'
s1 = 'SNE'
s2 = 'MCD'
s3 = 'TGT'
index = '^IXIC'
#Start = input("Please input start date(yyyy-mm-dd): ")
#End = input("Please input end date (yyyy-mm-dd): ")
Start = '2018-02-24'
End = '2018-09-03'
Start1 = adjDate(Start)
End1 = adjDate(End)

tb = quandl.get("FED/RIFSGFSM06_N_WF", start_date=Start1, end_date=End1)

def get_data1(ticker):
    data = yf(ticker)
    stock = data.get_historical_price_data(Start, End, 'weekly')
    keys = list(stock.keys())
    
    stock1 = stock[keys[0]]
    list1 = list(stock1.keys())
    a1 = stock1[list1[5]]
    num_a1 = len(a1)
    i = 0
    price = []
    date = []
    for i in range (num_a1):
        data1 = a1[i]
        data1_keys = list(data1.keys())
        p = data1[data1_keys[6]]
        d = data1[data1_keys[7]]
        price.append(p)
        date.append(d)
        i += 1
    return price, date


def get_data(ticker):
    data = yf(ticker)
    stock = data.get_historical_price_data(Start, End, 'weekly')
    keys = list(stock.keys())
    
    stock1 = stock[keys[0]]
    list1 = list(stock1.keys())
    a1 = stock1[list1[5]]
    num_a1 = len(a1)
    i = 0
    price = []
    date = []
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

stock1 = get_data(s1)
stock2 = get_data(s2)
stock3 = get_data(s3)
index1 = get_data(index)

data1 = get_data1(s1)
data2 = get_data1(s2)
data3 = get_data1(s3)
data4 = get_data1(index)

p1 = data1[0]
p2 = data2[0]
p3 = data3[0]
p4 = data4[0]
date1 = data1[1]
data = pd.DataFrame({"Date": date1, s1:p1, s2:p2, s3:p3, "NASDAQ":p4})
data = data.set_index("Date", drop=False)
del data["Date"]
data = data.dropna()

def HPR_cal(var1):
    dr1 = (var1.Close.shift(1) - var1.Close)/stock1.Close
    var1['Discrete(HPR)'] = dr1
    return var1

# dr1 = HPR_cal(stock1)
# dr2 = HPR_cal(stock2)
# dr3 = HPR_cal(stock3)
# dr4 = HPR_cal(index1)
# print("@001", dr1)

def HPR(data,i):
    hpr = (data.Close.iloc[i+1]-data.Close.iloc[i])/data.Close.iloc[i]
    return hpr

dr1 = [np.nan]
dr2 = [np.nan]
dr3 = [np.nan]
dr4 = [np.nan]
#
#print("Here")
for x in range(0,27):
    dr1.append(HPR(stock1,x))
stock1['Discrete(HPR)'] = dr1
print("@001", dr1)
                                                           
for x in range(0,27):
    dr2.append(HPR(stock2,x))
stock2['Discrete(HPR)'] = dr2  

for x in range(0,27):
    dr3.append(HPR(stock3,x))
stock3['Discrete(HPR)'] = dr3  

for x in range(0,27):
    dr4.append(HPR(index1,x))
index1['Discrete(HPR)'] = dr4  


ddr1 = pd.DataFrame(dr1)
ddr2 = pd.DataFrame(dr2)
ddr3 = pd.DataFrame(dr3)
ddr4 = pd.DataFrame(dr4)
ddr1, ddr2, ddr3, ddr4 = ddr1.dropna(), ddr2.dropna(), ddr3.dropna(), ddr4.dropna() 
er = pd.concat([ddr1, ddr2, ddr3, ddr4], axis=1)
er.columns = [s1, s2, s3, 'NASDAQ']

er.fillna('', inplace=True)

hdr1 = pd.Series.as_matrix(ddr1)
hdr2 = pd.Series.as_matrix(ddr2)
hdr3 = pd.Series.as_matrix(ddr3)
hdr4 = pd.Series.as_matrix(ddr4)

hdr1 = hdr1[~np.isnan(hdr1)]
hdr2 = hdr2[~np.isnan(hdr2)]
hdr3 = hdr3[~np.isnan(hdr3)]
hdr4 = hdr4[~np.isnan(hdr4)]

def arm(var1):
    return sum(var1) / len(var1)

am1 = arm(hdr1)
am2 = arm(hdr2)
am3 = arm(hdr3)
am4 = arm(hdr4)

ndr1 = 1 + hdr1
ndr2 = 1 + hdr2
ndr3 = 1 + hdr3
ndr4 = 1 + hdr4

def geo_mean(var1):
    a = np.array(var1)
    return (a.prod()**(1/len(a)))-1
gm1 = geo_mean(ndr1)
gm2 = geo_mean(ndr2)
gm3 = geo_mean(ndr3)
gm4 = geo_mean(ndr4)

vr1 = np.var(hdr1)
vr2 = np.var(hdr2)
vr3 = np.var(hdr3)
vr4 = np.var(hdr4)

sd1 = np.std(hdr1)
sd2 = np.std(hdr2)
sd3 = np.std(hdr3)
sd4 = np.std(hdr4)

cal1 = ((am1, am2, am3, am4),(gm1, gm2, gm3, gm4), (vr1, vr2, vr3, vr4), (sd1, sd2, sd3, sd4))
cal1 = pd.DataFrame(list(cal1), columns = [s1, s2, s3,'NASDAQ'], index=['Arithmetic Mean',
                    'Geometic Mean', 'Variance','Standard Deviation'])

w = hdr1 #s1
x = hdr2 #s2
y = hdr3 #s3
z = hdr4 #NASDAQ
sx1 = np.stack((w, x, y, z), axis=0)

c = np.cov(sx1)
c = pd.DataFrame(c, columns=[s1, s2, s3,'NASDAQ'], index=[s1, s2, s3,'NASDAQ'])

def mean(w):
    return sum(w) / len(w)

def cov(var1, var2):
    var1_mean = mean(var1)
    var2_mean = mean(var2)
    data = [(var1[i] - var1_mean) * (var2[i] - var2_mean)
            for i in range(len(var1))]
    return sum(data) / (len(data))

cov1 = cov(w, x)
cov2 = cov(w, y)
cov3 = cov(x, y)
cov4 = cov(y, z)
cov5 = cov(z, x)
cov6 = cov(z, w)
covg = ((cov1),(cov2),(cov3),(cov4),(cov5),(cov6))
cov = pd.DataFrame(list(covg), columns=[''], index=['Covariance('+s1+','+s2+')',
                   'Covariance('+s1+','+s3+')','Covariance('+s2+','+s3+')', 'Covariance('+s3+',NASDAQ)',
                   'Covariance(NASDAQ,'+s2+')','Covariance(NASDAQ,'+s1+')'])

cc = corrcoef([w, x, y, z])
cc = pd.DataFrame(list(cc), columns = [s1, s2, s3,'NASDAQ'], index=[s1, s2, s3,'NASDAQ'])

cc1 = stats.pearsonr(w,x) #s1, s2
cc2 = stats.pearsonr(w,y) #s1, s3
cc3 = stats.pearsonr(w,z) #s1, NASDAQ
cc4 = stats.pearsonr(x,y) #s2, s3
cc5 = stats.pearsonr(x,z) #s2, NASDAQ
cc6 = stats.pearsonr(y,z) #s3, NASDAQ

cc1 = list(cc1)
del cc1[-1]
cc2 = list(cc2)
del cc2[-1]
cc3 = list(cc3)
del cc3[-1]
cc4 = list(cc4)
del cc4[-1]
cc5 = list(cc5)
del cc5[-1]
cc6 = list(cc6)
del cc6[-1]

cc7 = ((cc1),(cc2),(cc3),(cc4),(cc5),(cc6))
ccf = pd.DataFrame(list(cc7), columns=[''], index=['Correlation Coefficients('+s1+','+s2+')',
                   'Correlation Coefficients('+s1+','+s3+')', 'Correlation Coefficients('+s1+',NASDAQ)',
                   'Correlation Coefficients('+s2+','+s3+')', 'Correlation Coefficients('+s2+',NASDAQ)',
                   'Correlation Coefficients('+s3+',NASDAQ)'])

w1 = (1.0/3.0)
w2 = (1.0/3.0)
w3 = (1.0/3.0)
nw1 = (1.0/3.0)**2
nw2 = (1.0/3.0)**2
nw3 = (1.0/3.0)**2
wei= (((w1),(w2),(w3)),((nw1),(nw2),(nw3)))
nwei = pd.DataFrame(list(wei), columns=[s1, s2, s3], index=['Weight', 'Weight^2'])

# Portfolio Return
#------------------------------------------------------------------------------
avgr1 = np.mean(hdr1)
avgr2 = np.mean(hdr2)
avgr3 = np.mean(hdr3)
#
pr = (w1*avgr1) + (w2*avgr2) + (w3*avgr3)

# Portfolio Variance 
#------------------------------------------------------------------------------
# σp^2= (W1^2*σ1^2) + (W2^2*σ2^2) + (W3^2*σ3^2) + (2*W1*W2*Cov(r1,r2)) + (2*W1*W3*Cov(r1,r3)) + (2*W2*W3*Cov(r2,r3))
pv = (nw1*vr1) + (nw1*vr2) + (nw3*vr3) + (2.0*nw1*nw2*cov1) + (2.0*nw1*nw3*cov2) + (2.0*nw2*nw3*cov3)

# Portfolio Standard Deviation 
#------------------------------------------------------------------------------
psd = math.sqrt(pv)

rrp = ((pr),(pv),(psd))
pf = pd.DataFrame(list(rrp), columns=[''], index=['Portfolio Return','Portfolio Variance',
                  'Portfolio Standard Deviation']) 

## Into Microsoft EXCEL
##______________________________________________________________________________
writer = pd.ExcelWriter('Portfolio_Management.xlsx', engine = 'xlsxwriter',
                        date_format='dd mm yyy')

data.to_excel(writer, sheet_name='Closing Price')
stock1.to_excel(writer, sheet_name=s1)
stock2.to_excel(writer, sheet_name=s2)
stock3.to_excel(writer, sheet_name=s3)
index1.to_excel(writer, sheet_name='NASDAQ')
tb.to_excel(writer, sheet_name='Treasury Bill')
er.to_excel(writer, sheet_name='Discrete Return')
cal1.to_excel(writer, sheet_name='Appendix 1')
c.to_excel(writer, sheet_name='Appendix 2')
cov.to_excel(writer, sheet_name='Appendix 3')
cc.to_excel(writer, sheet_name='Appendix 4')
ccf.to_excel(writer, sheet_name='Appendix 5')
nwei.to_excel(writer, sheet_name='Appendix 6')
pf.to_excel(writer, sheet_name='Appendix 7')



# print("Calculation complete. Saving...")
writer.save()
# time.sleep(5)
# print("Saved")
# time.sleep(2)

# sys.exit

