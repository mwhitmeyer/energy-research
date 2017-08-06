# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 15:10:04 2017

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

summerhours = set() 
winterhours = set()

for t in summer.time:
    summerhours.add(t)
    
for t in winter.time:
    winterhours.add(t)
    
#make the set an ordered list (so that the zip function performs the way we desire it to)
    
summerhours = list(summerhours)
summerhours.sort()

winterhours = list(winterhours)
winterhours.sort()

# Use histograms for summer months
"""for hour, k in zip(summerhours, range(24)):
    plt.figure(figsize=(12,8))  
    x = totalhourlysummer.loc[hour]
    (a,b,loc,scale)=stats.beta.fit(x['use'], loc=0, fscale = x['use'].max())
    evenspaced = np.linspace(0, x['use'].max(), 100)
    pdf = stats.beta.pdf(evenspaced, a, b, loc = loc, scale = scale)  
    plt.plot(evenspaced, pdf)
    plt.hist(x['use'], normed = True)
    plt.xlabel('Total Use (Kilowatts)') 
    plt.ylabel('Probability Density')
    plt.title('Summer Load Histogram for ' + str(k) + ':00')"""
    
#Generation histograms for summer months
"""for hour, k in zip(summerhours, range(24)):
    plt.figure(figsize=(12,8)) 
    x = totalhourlysummer.loc[hour]
    (a,b,loc,scale)=stats.beta.fit(x['gen'], loc=0, fscale = x['gen'].max())
    evenspaced = np.linspace(0, x['gen'].max(), 100)
    pdf = stats.beta.pdf(evenspaced, a, b, loc = loc, scale = scale) 
    plt.plot(evenspaced, pdf)
    plt.hist(x['gen'], normed = True)
    plt.xlabel('Total Generation (Kilowatts)') 
    plt.ylabel('Number of Days')
    plt.title('Summer PV Generation Histogram for ' + str(k) + ':00')"""
    
# Use histograms for winter months
"""for hour, k in zip(winterhours, range(24)):
    plt.figure(figsize=(12,8)) 
    x = totalhourlywinter.loc[hour]
    (a,b,loc,scale)=stats.beta.fit(x['use'], loc=0, fscale = x['use'].max())
    evenspaced = np.linspace(0, x['use'].max(), 100)
    pdf = stats.beta.pdf(evenspaced, a, b, loc = loc, scale = scale) 
    plt.plot(evenspaced, pdf)
    plt.hist(x['use'], normed = True)
    plt.xlabel('Total Use (Kilowatts)') 
    plt.ylabel('Number of Days')
    plt.title('Winter Load Histogram for ' + str(k) + ':00')"""
    
#Generation histograms for winter months
#for hour, k in zip(winterhours, range(24)):
#    plt.figure(figsize=(12,8)) 
#    x = totalhourlywinter.loc[hour]
#    kde = stats.gaussian_kde(x['gen'])
#    evenspaced = np.linspace(0, x['gen'].max(), 100)
#    pdf = kde.pdf(evenspaced)
#    """sorted1 = x['gen'].sort_values().head(x['gen'].count() // 2)
#    sorted2 = x['gen'].sort_values().tail(x['gen'].count() // 2)
#    (a1, b1) = stats.norm.fit(sorted1, loc=0, fscale = x['gen'].median())
#    (a2, b2, loc2, scale2) = stats.beta.fit(sorted2, loc = x['gen'].median() , fscale = x['gen'].max())
#    evenspaced1 = np.linspace(0, x['gen'].max() / 2, 100)
#    evenspaced2 = np.linspace(x['gen'].max() / 2, x['gen'].max(), 100)
#    pdf1 = stats.norm.pdf(evenspaced1, a1, b1) 
#    pdf2 = stats.beta.pdf(evenspaced2, a2, b2, loc = loc2, scale = scale2) 
#    plt.plot(evenspaced1, pdf1)
#    plt.plot(evenspaced2, pdf2)"""
#    plt.plot(evenspaced, pdf)
#    plt.hist(x['gen'], normed = True, bins = 20)
#    plt.ylabel('Number of Days')
#    plt.title('Winter PV Generation Histogram for ' + str(k) + ':00')
    
for hour, k in zip(summerhours, range(24)):
    plt.figure(figsize=(12,8))  
    x = totalhourlysummer.loc[hour]
    kde = stats.gaussian_kde(x['use'])
    evenspaced = np.linspace(0, x['use'].max(), 100)
    pdf = kde.pdf(evenspaced)  
    plt.axvline(np.percentile(x['use'], 95), linestyle = '--', color = 'r')
    plt.plot(evenspaced, pdf)
    plt.hist(x['use'], normed = True)
    plt.xlabel('Total Use (Kilowatts)') 
    plt.ylabel('Probability Density')
    plt.title('Summer Load Histogram for ' + str(k) + ':00')


