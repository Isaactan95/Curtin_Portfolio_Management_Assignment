from utilites import utilites as uti
from calculation import Calculation as cal
import pandas as pd, numpy as np
from toExcel import ToExcel 

class Main():

    def __init__(self):
        self.ticker1 = 'SNE' #input("Ticker 1: ")
        self.ticker2 = 'MCD' #input("Ticker 2: ")
        self.ticker3 = 'TGT' #input("Ticker 3: ")
        self.index = '^IXIC'
        self.start = '2018-02-24' #input("Start date (yyyy-mm-dd): ")
        self.end = '2018-09-03' #input("End date (yyyy-mm-dd): ")
        self.start1 = uti.adjDate(self.start)
        self.end1 = uti.adjDate(self.end)
        self.main()

    def main(self):
        self.tb = uti.getTB(self.start1, self.end1)
        self.stock1 = uti.get_data(self.ticker1, self.start, self.end)
        self.stock2 = uti.get_data(self.ticker2, self.start, self.end)
        self.stock3 = uti.get_data(self.ticker3, self.start, self.end)
        self.index1 = uti.get_data(self.index, self.start, self.end)

        self.data1 = uti.get_data1(self.ticker1, self.start, self.end)
        self.data2 = uti.get_data1(self.ticker2, self.start, self.end)
        self.data3 = uti.get_data1(self.ticker3, self.start, self.end)
        self.data4 = uti.get_data1(self.index, self.start, self.end)

        self.p1 = self.data1[0]
        self.p2 = self.data2[0]
        self.p3 = self.data3[0]
        self.p4 = self.data4[0]
        self.date = self.data1[1]

        self.data = pd.DataFrame({"Date": self.date, 
            self.ticker1:self.p1, self.ticker2:self.p2, self.ticker3:self.p3,
             "NASDAQ":self.p4})
        self.data = self.data.set_index("Date", drop=False)
        del self.data["Date"]
        self.data = self.data.dropna()

        self.dr1 = [np.nan]
        self.dr2 = [np.nan]
        self.dr3 = [np.nan]
        self.dr4 = [np.nan]

        cal().HPR(self.dr1, self.stock1)
        cal().HPR(self.dr2, self.stock2)
        cal().HPR(self.dr3, self.stock3)
        cal().HPR(self.dr4, self.index1)

        self.stock1['Discrete(HPR)'] = self.dr1
        self.stock2['Discrete(HPR)'] = self.dr2
        self.stock3['Discrete(HPR)'] = self.dr3
        self.index1['Discrete(HPR)'] = self.dr4

        self.ddr1 = pd.DataFrame(self.dr1)
        self.ddr2 = pd.DataFrame(self.dr2)
        self.ddr3 = pd.DataFrame(self.dr3)
        self.ddr4 = pd.DataFrame(self.dr4)
        self.ddr1 = self.ddr1.dropna()
        self.ddr2 = self.ddr2.dropna()
        self.ddr3 = self.ddr3.dropna()
        self.ddr4 = self.ddr4.dropna()
        self.er = pd.concat([self.ddr1, self.ddr2, self.ddr3, self.ddr4], axis=1)
        self.er.columns = [self.ticker1, self.ticker2, self.ticker3, 'NASDAQ']
        self.er.fillna('', inplace=True)


        self.hdr1 = pd.Series.as_matrix(self.ddr1)
        self.hdr2 = pd.Series.as_matrix(self.ddr2)
        self.hdr3 = pd.Series.as_matrix(self.ddr3)
        self.hdr4 = pd.Series.as_matrix(self.ddr4)

        self.hdr1 = self.hdr1[~np.isnan(self.hdr1)]
        self.hdr2 = self.hdr2[~np.isnan(self.hdr2)]
        self.hdr3 = self.hdr3[~np.isnan(self.hdr3)]
        self.hdr4 = self.hdr4[~np.isnan(self.hdr4)]

        self.am1 = cal().arm(self.hdr1)
        self.am2 = cal().arm(self.hdr2)
        self.am3 = cal().arm(self.hdr3)
        self.am4 = cal().arm(self.hdr4)

        self.gm1 = cal().geo_mean((self.hdr1+1))
        self.gm2 = cal().geo_mean((self.hdr2+1))
        self.gm3 = cal().geo_mean((self.hdr3+1))
        self.gm4 = cal().geo_mean((self.hdr4+1))

        self.vr1 = cal().variance(self.hdr1)
        self.vr2 = cal().variance(self.hdr2)
        self.vr3 = cal().variance(self.hdr3)
        self.vr4 = cal().variance(self.hdr4)

        self.sd1 = cal().stDeviation(self.hdr1)
        self.sd2 = cal().stDeviation(self.hdr2)
        self.sd3 = cal().stDeviation(self.hdr3)
        self.sd4 = cal().stDeviation(self.hdr4)

        self.cal1 = ((self.am1, self.am2, self.am3, self.am4),
            (self.gm1, self.gm2, self.gm3, self.gm4), 
            (self.vr1, self.vr2, self.vr3, self.vr4), 
            (self.sd1, self.sd2, self.sd3, self.sd4))
        self.cal1 = pd.DataFrame(list(self.cal1), columns = [self.ticker1, self.ticker2, self.ticker3,'NASDAQ'], 
            index=['Arithmetic Mean', 'Geometic Mean', 'Variance','Standard Deviation'])

        self.sx1 = np.stack((self.hdr1, self.hdr2, self.hdr3, self.hdr4), axis=0)
        self.c = np.cov(self.sx1)
        self.c = pd.DataFrame(self.c, 
            columns=[self.ticker1, self.ticker2, self.ticker3, 'NASDAQ'], 
            index=[self.ticker1, self.ticker2, self.ticker3, 'NASDAQ'])

        self.cov1 = cal().cov(self.hdr1, self.hdr2)
        self.cov2 = cal().cov(self.hdr1, self.hdr3)
        self.cov3 = cal().cov(self.hdr2, self.hdr3)
        self.cov4 = cal().cov(self.hdr3, self.hdr4)
        self.cov5 = cal().cov(self.hdr4, self.hdr2)
        self.cov6 = cal().cov(self.hdr4, self.hdr1)
        self.covg = ((self.cov1),(self.cov2),   
            (self.cov3),(self.cov4),(self.cov5),(self.cov6))

        self.cov = pd.DataFrame(list(self.covg), columns=[''], 
            index=[f'Covariance({self.ticker1},{self.ticker2})',
            f'Covariance({self.ticker1},{self.ticker3})',
            f'Covariance({self.ticker2},{self.ticker3})', 
            f'Covariance({self.ticker3},NASDAQ)',f'Covariance(NASDAQ,{self.ticker2})',
            f'Covariance(NASDAQ,{self.ticker1})'])

        self.cc = cal().corr([self.hdr1, self.hdr2, self.hdr3, self.hdr4])
        self.cc = pd.DataFrame(list(self.cc), 
            columns = [self.ticker1, self.ticker2, self.ticker3,'NASDAQ'], 
            index=[self.ticker1, self.ticker2, self.ticker3,'NASDAQ'])

        self.cc1 = list(cal().pearsonCal(self.hdr1,self.hdr2))
        del self.cc1[-1]
        self.cc2 = list(cal().pearsonCal(self.hdr1,self.hdr3))
        del self.cc2[-1]
        self.cc3 = list(cal().pearsonCal(self.hdr1,self.hdr4))
        del self.cc3[-1]
        self.cc4 = list(cal().pearsonCal(self.hdr2,self.hdr3))
        del self.cc4[-1]
        self.cc5 = list(cal().pearsonCal(self.hdr2,self.hdr4))
        del self.cc5[-1]
        self.cc6 = list(cal().pearsonCal(self.hdr3,self.hdr4))
        del self.cc6[-1]
        self.cc7 = ((self.cc1),(self.cc2),(self.cc3),
            (self.cc4),(self.cc5),(self.cc6))
        self.ccf = pd.DataFrame(list(self.cc7), columns=[''], 
            index=[f'Correlation Coefficients({self.ticker1},{self.ticker2})',
                   f'Correlation Coefficients({self.ticker1},{self.ticker3})', 
                   f'Correlation Coefficients({self.ticker1},NASDAQ)',
                   f'Correlation Coefficients({self.ticker2},{self.ticker3})',
                   f'Correlation Coefficients({self.ticker2},NASDAQ)',
                   f'Correlation Coefficients({self.ticker3},NASDAQ)'])
        self.weight = (1.0/3.0)
        self.nweight = (1.0/3.0)**2
        self.wei = (((self.weight),(self.weight),(self.weight)),
            ((self.nweight),(self.nweight),(self.nweight)))
        self.wei = pd.DataFrame(list(self.wei), 
            columns=[self.ticker1, self.ticker2, self.ticker3], 
            index=['Weight', 'Weight^2'])

        self.avgr1 = cal().avg(self.hdr1)
        self.avgr2 = cal().avg(self.hdr2)
        self.avgr3 = cal().avg(self.hdr3)
        self.pr = (self.weight*self.avgr1) + (self.weight*self.avgr2) + (self.weight*self.avgr3)
        self.pv = (self.nweight*self.vr1) + (self.nweight*self.vr2) + (self.nweight*self.vr3) + (2.0*self.nweight*self.nweight*self.cov1) + (2.0*self.nweight*self.nweight*self.cov2) + (2.0*self.nweight*self.nweight*self.cov3)
        self.psd = cal().portSD(self.pv)
        self.rrp = ((self.pr),(self.pv),(self.psd))
        self.pf = pd.DataFrame(list(self.rrp), 
            columns=[''], index=['Portfolio Return','Portfolio Variance',
                  'Portfolio Standard Deviation'])

        ToExcel(self.ticker1, self.ticker2, self.ticker3, self.data, 
            self.stock1, self.stock2, self.stock3, self.index1, self.tb, self.er, 
            self.cal1, self.c, self.cov, self.cc, self.ccf, self.wei, self.pf).writeFile()

if __name__ == "__main__":
    Main()