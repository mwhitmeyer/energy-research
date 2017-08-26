# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 21:38:51 2017

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


# creating an empty set and then putting all of the time values into it

winterhours = set()
    
for t in winter.time:
    winterhours.add(t)
    
#make the set an ordered list (so that the zip function performs the way we desire it to)

winterhours = list(winterhours)
winterhours.sort()

toWrite = pd.DataFrame()
maxUseOrGen = max(totalhourlywinter['gen'].max(), totalhourlywinter['use'].max(), 
                  totalhourlysummer['gen'].max(), totalhourlysummer['use'].max())
evenspaced = np.linspace(0, maxUseOrGen, 100)
toWrite['power'] = evenspaced

    
#Generation histograms for winter months
for hour, k in zip(winterhours, range(24)):
    plt.figure(figsize=(12,8)) 
    x = totalhourlywinter.loc[hour]
    kde = stats.gaussian_kde(x['use'], 0.35)
    pdf = kde.pdf(evenspaced)
    toWrite[str(k) + ':00 pdf'] = pdf
    plt.axvline(np.percentile(x['use'], 95), linestyle = '--', color = 'r')
    plt.plot(evenspaced, pdf)
    plt.hist(x['use'], normed = True)
    plt.ylabel('Number of Days')
    plt.title('Winter Use Histogram for ' + str(k) + ':00')
    
toWrite.to_csv('winteruse.csv')