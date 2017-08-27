# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 21:38:48 2017

@author: whitt
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

summer = pd.read_csv('Summer2016-30houses.csv')

winter = pd.read_csv('Winter2016-2017-30houses.csv')

summer['date'], summer['time'] = summer['localminute'].str.split(' ', 1).str

winter['date'], winter['time'] = winter['localminute'].str.split(' ', 1).str

#group by the hour, then by the date, and sum the use and gen for each household

totalhourlysummer = summer.groupby(['time', 'date']).sum()

totalhourlywinter = winter.groupby(['time', 'date']).sum()

summerhours = set()
    
for t in summer.time:
    summerhours.add(t)
    
#make the set an ordered list (so that the zip function performs the way we desire it to)

summerhours = list(summerhours)
summerhours.sort()

toWrite = pd.DataFrame()
maxUseOrGen = max(totalhourlywinter['gen'].max(), totalhourlywinter['use'].max(), 
                  totalhourlysummer['gen'].max(), totalhourlysummer['use'].max())
evenspaced = np.arange(0, maxUseOrGen + 1, 1)
toWrite['power'] = evenspaced

for hour, k in zip(summerhours, range(24)):
    plt.figure(figsize=(12,8)) 
    x = totalhourlysummer.loc[hour]
    kde = stats.gaussian_kde(x['use'], .35)
#    print(kde.integrate_box_1d(0, maxUseOrGen))
    pdf = kde.pdf(evenspaced)
    print(np.trapz(pdf, dx = maxUseOrGen/(evenspaced.size - 1)))
    toWrite[str(k) + ':00 pdf'] = pdf
    plt.axvline(np.percentile(x['use'], 95), linestyle = '--', color = 'r')
    plt.plot(evenspaced, pdf)
    plt.hist(x['use'], normed = True)
    plt.ylabel('Number of Days')
    plt.title('Summer Use Histogram for ' + str(k) + ':00')

toWrite.to_csv('summeruse.csv')