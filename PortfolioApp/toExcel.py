import pandas as pd

class ToExcel():

    def __init__(self, ticker1, ticker2, ticker3, data, stock1, stock2, 
        stock3, index, tb, er, cal1, c, cov, cc, ccf, nwei, pf):
        self.ticker1 = ticker1
        self.ticker2 = ticker2
        self.ticker3 = ticker3
        self.data = data
        self.stock1 = stock1
        self.stock2 = stock2
        self.stock3 = stock3
        self.index = index
        self.tb = tb
        self.er = er
        self.cal1 = cal1
        self.c = c
        self.cov = cov
        self.cc = cc
        self.ccf = ccf
        self.nwei = nwei
        self.pf = pf

    def writeFile(self):
        writer = pd.ExcelWriter('Portfolio_Management.xlsx', engine = 'xlsxwriter',
                        date_format='dd mm yyy')
        self.data.to_excel(writer, sheet_name='Closing Price')
        self.stock1.to_excel(writer, sheet_name=self.ticker1)
        self.stock2.to_excel(writer, sheet_name=self.ticker2)
        self.stock3.to_excel(writer, sheet_name=self.ticker3)
        self.index.to_excel(writer, sheet_name='NASDAQ')
        self.tb.to_excel(writer, sheet_name='Treasury Bill')
        self.er.to_excel(writer, sheet_name='Discrete Return')
        self.cal1.to_excel(writer, sheet_name='Appendix 1')
        self.c.to_excel(writer, sheet_name='Appendix 2')
        self.cov.to_excel(writer, sheet_name='Appendix 3')
        self.cc.to_excel(writer, sheet_name='Appendix 4')
        self.ccf.to_excel(writer, sheet_name='Appendix 5')
        self.nwei.to_excel(writer, sheet_name='Appendix 6')
        self.pf.to_excel(writer, sheet_name='Appendix 7')
        writer.save()