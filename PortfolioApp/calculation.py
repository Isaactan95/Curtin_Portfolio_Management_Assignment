import pandas as pd, numpy as np, math
from scipy import stats


class Calculation():

    def __init__(self):
        pass

    def HPR_cal(self, dataframe):
        data = (dataframe.Close.shift(1) - dataframe.Close)/dataframe.Close
        dataframe['Discrete(HPR)'] = data
        return dataframe

    def calHPR(self, data, i):
        hpr = (data.Close.iloc[i+1] - data.Close.iloc[i])/ data.Close.iloc[i]
        return hpr

    def HPR(self, dr, data):
        for x in range(0, 27):
            dr.append(self.calHPR(data, x))
        return dr

    def matrix(self, data):
        dr = pd.Series.as_matrix(data)
        return dr

    def addNan(self, hdr):
        data = hdr1[~np.isnan(hdr1)]
        return data

    def arm(self, var1):
        return sum(var1) / len(var1)

    def geo_mean(self, var1):
        a = np.array(var1)
        return (a.prod()**(1/len(a)))-1

    def variance(self, hdr):
        data = np.var(hdr)
        return data

    def stDeviation(self, hdr):
        data = np.std(hdr)
        return data

    def mean(self, var):
        return sum(var)/len(var)

    def cov(self, var1, var2):
        var1_mean = self.mean(var1)
        var2_mean = self.mean(var2)
        data = [(var1[i] - var1_mean) * (var2[i] - var2_mean)
                for i in range(len(var1))]
        return sum(data) / (len(data))

    def corr(self, args):
        data = np.corrcoef(args)
        return data

    def pearsonCal(self, var1, var2):
        data = stats.pearsonr(var1, var2)
        return data

    def avg(self, var):
        data = np.mean(var)
        return data

    def portReturn(self, avg1, avg2, avg3, w, nw):
        portfolioReturn = (w*avg1) + (w*avg2) + (w*avg3)
        return portfolioReturn

    def portVariance(self, nw, vr1, vr2, vr3, cov1, cov2, cov3):
        # σp^2= (W1^2*σ1^2) + (W2^2*σ2^2) + (W3^2*σ3^2) + (2*W1*W2*Cov(r1,r2)) + (2*W1*W3*Cov(r1,r3)) + (2*W2*W3*Cov(r2,r3))
        pv1 = (nw*vr1) + (nw*vr2) + (nw*vr3)
        pv2 = (2.0*nw*nw*cov1) + (2.0*nw*nw*cov2) + (2.0*nw*nw*cov3)
        pv = pv1 + pv2
        return pv

    def portSD(self, pv):
        sd = math.sqrt(pv)
        return sd