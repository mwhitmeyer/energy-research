# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 18:30:55 2017

@author: whitt
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import time

current_milli_time = lambda: int(round(time.time() * 1000))

initialtime = current_milli_time()

threeyears = pd.read_csv('12012013-08312016thirtyhomes1.csv')

#get rid of timezone at the end of the localminute obj ('00:00:00-05' --> '00:00:00')
threeyears['localminute'] = [row[1][:len(row[1]) - 3] for row in threeyears.itertuples()] 

threeyears['date'], threeyears['time'] = threeyears['localminute'].str.split(' ', 1).str

#threeyears['localminute'] = [pd.to_datetime(row[1]) for row in threeyears.itertuples()]


# group by date and time, then sum. 
# Lets us easily choose the date range, and then group by time and date
gbDate = threeyears.groupby(['date', 'time']).sum()


def getAllWinterData():
    getWinterGen()
    getWinterLoad()
    

    
def getWinterGen():
    # get the three winters, then group by the hour
    winter1 = gbDate.loc['2013-12-01':'2014-02-28', ['use', 'gen']]
    winter1 = winter1.groupby(['time', 'date']).sum()
    winter2 = gbDate.loc['2014-12-01':'2015-02-28', ['use', 'gen']]
    winter2 = winter2.groupby(['time', 'date']).sum()
    winter3 = gbDate.loc['2015-12-01':'2016-02-28', ['use', 'gen']]
    winter3 = winter3.groupby(['time', 'date']).sum()
    
    # make a sorted list of hours that we iterate through later in the for loop
    hours = set()
    count = 0
    for row in gbDate.iterrows():
        hours.add(row[0][1])
        if count == 24:
            break;
        count += 1
    hours = list(hours)
    hours.sort()
    
    #initiate a dataframe for the actual summed gen values in the three winters for every hour
    #temp = winter2.loc['13:00:00'].index #list of all the dates
    #temp = [x[5:] for x in temp] #get rid of the year part of the date (2013-12-01 --> 12-01)
    temp = winter1.index.levels[1].append(winter2.index.levels[1].append(winter3.index.levels[1]))
    summedvals = pd.DataFrame(index = hours, columns = temp) #initiate dataframe
    summedvals.fillna(0, inplace = True) #replace NaN with zeros
        
    
    # initiate the dataframe for the pdf values that we will write to the csv
    pdfvals = pd.DataFrame()
    # find the max power value for our PDF and histograms
    maxUseOrGen = max(gbDate['gen'].max(), gbDate['use'].max())
    # for our PDF, with step size of 1
    evenspaced = np.arange(0, maxUseOrGen + 1, 1)
    # the first column of our data frame with the evenly spaced power values
    pdfvals['power'] = evenspaced
    
    # plots a histogram and a pdf for the KDE, and puts the pdf value in pdfvals
    for hour, k in zip(hours[7:20], range(7, 20)):
        plt.figure(figsize=(12,8)) 
        x1 = winter1.loc[hour]['gen']
        x2 = winter2.loc[hour]['gen']
        x3 = winter3.loc[hour]['gen']
        for date in x1.index:
            #fill in the dataframe with the sum of each of the three winters (at corresponding date and time)
            summedvals[date][hour] += x1[date]
        for date in x2.index:
            summedvals[date][hour] += x2[date]
        for date in x3.index:
            summedvals[date][hour] += x3[date]
        #combine the three winters of data
        combined = x1.append(x2).append(x3)
        kde = stats.gaussian_kde(combined, 0.35)
        pdf = kde.pdf(evenspaced)
        pdfvals[str(k) + ':00 pdf'] = pdf
        plt.axvline(np.percentile(combined, 95), linestyle = '--', color = 'r')
        plt.plot(evenspaced, pdf)
        plt.hist(combined, normed = True)
        plt.ylabel('Probability Density')
        plt.title('Winter PV Generation Histogram for ' + str(k) + ':00')
    
    pdfvals.to_csv('threewintersgen.csv')
    summedvals.T.to_csv('threewintersgensummed.csv')
    
def getWinterLoad():
    winter1 = gbDate.loc['2013-12-01':'2014-02-28', ['use', 'gen']]
    winter1 = winter1.groupby(['time', 'date']).sum()
    winter2 = gbDate.loc['2014-12-01':'2015-02-28', ['use', 'gen']]
    winter2 = winter2.groupby(['time', 'date']).sum()
    winter3 = gbDate.loc['2015-12-01':'2016-02-28', ['use', 'gen']]
    winter3 = winter3.groupby(['time', 'date']).sum()
    
    hours = set()
    count = 0
    for row in gbDate.iterrows():
        hours.add(row[0][1])
        if count == 24:
            break;
        count += 1
    hours = list(hours)
    hours.sort()
    
#    temp = winter2.loc['13:00:00'].index
 #   temp = [x[5:] for x in temp]
    temp = winter1.index.levels[1].append(winter2.index.levels[1].append(winter3.index.levels[1]))
    summedvals = pd.DataFrame(index = hours, columns = temp)
    summedvals.fillna(0, inplace = True)
    
    pdfvals = pd.DataFrame()
    maxUseOrGen = max(gbDate['gen'].max(), gbDate['use'].max())
    evenspaced = np.arange(0, maxUseOrGen + 1, 1)
    pdfvals['power'] = evenspaced
    
    for hour, k in zip(hours, range(24)):
        plt.figure(figsize=(12,8)) 
        x1 = winter1.loc[hour]['use']
        x2 = winter2.loc[hour]['use']
        x3 = winter3.loc[hour]['use']
        for date in x1.index:
            #fill in the dataframe with the sum of each of the three winters (at corresponding date and time)
            summedvals[date][hour] += x1[date]
        for date in x2.index:
            summedvals[date][hour] += x2[date]
        for date in x3.index:
            summedvals[date][hour] += x3[date]
        combined = x1.append(x2).append(x3)
        kde = stats.gaussian_kde(combined, 0.35)
        pdf = kde.pdf(evenspaced)
        pdfvals[str(k) + ':00 pdf'] = pdf
        plt.axvline(np.percentile(combined, 95), linestyle = '--', color = 'r')
        plt.plot(evenspaced, pdf)
        plt.hist(combined, normed = True)
        plt.ylabel('Probability Density')
        plt.title('Winter Load Histogram for ' + str(k) + ':00')
    
    pdfvals.to_csv('threewintersuse.csv')
    summedvals.T.to_csv('threewintersusesummed.csv')

def getAllSummerData():
    getSummerGen()
    getSummerLoad()
    
def getSummerGen():
    summer1 = gbDate.loc['2014-06-01':'2014-08-30', ['use', 'gen']]
    summer1 = summer1.groupby(['time', 'date']).sum()
    summer2 = gbDate.loc['2015-06-01':'2015-08-30', ['use', 'gen']]
    summer2 = summer2.groupby(['time', 'date']).sum()
    summer3 = gbDate.loc['2016-06-01':'2016-08-30', ['use', 'gen']]
    summer3 = summer3.groupby(['time', 'date']).sum()
    
    hours = set()
    count = 0
    for row in gbDate.iterrows():
        hours.add(row[0][1])
        if count == 24:
            break;
        count += 1
    hours = list(hours)
    hours.sort()
    
#    temp = summer2.loc['13:00:00'].index
#    temp = [x[5:] for x in temp]
    temp = summer1.index.levels[1].append(summer2.index.levels[1].append(summer3.index.levels[1]))
    summedvals = pd.DataFrame(index = hours, columns = temp)
    summedvals.fillna(0, inplace = True)
    
    pdfvals = pd.DataFrame()
    maxUseOrGen = max(gbDate['gen'].max(), gbDate['use'].max())
    evenspaced = np.arange(0, maxUseOrGen + 1, 1)
    pdfvals['power'] = evenspaced
    
    for hour, k in zip(hours[6:21], range(6, 21)):
        plt.figure(figsize=(12,8)) 
        x1 = summer1.loc[hour]['gen']
        x2 = summer2.loc[hour]['gen']
        x3 = summer3.loc[hour]['gen']
        for date in x1.index:
            #fill in the dataframe with the sum of each of the three winters (at corresponding date and time)
            summedvals[date][hour] += x1[date]
        for date in x2.index:
            summedvals[date][hour] += x2[date]
        for date in x3.index:
            summedvals[date][hour] += x3[date]
        combined = x1.append(x2).append(x3)
        kde = stats.gaussian_kde(combined, 0.35)
        pdf = kde.pdf(evenspaced)
        pdfvals[str(k) + ':00 pdf'] = pdf
        plt.axvline(np.percentile(combined, 95), linestyle = '--', color = 'r')
        plt.plot(evenspaced, pdf)
        plt.hist(combined, normed = True)
        plt.ylabel('Probability Density')
        plt.title('Summer Generation Histogram for ' + str(k) + ':00')
    
    pdfvals.to_csv('threesummergen.csv')
    summedvals.T.to_csv('threesummergensummed.csv')
    
    
def getSummerLoad():
    summer1 = gbDate.loc['2014-06-01':'2014-08-30', ['use', 'gen']]
    summer1 = summer1.groupby(['time', 'date']).sum()
    summer2 = gbDate.loc['2015-06-01':'2015-08-30', ['use', 'gen']]
    summer2 = summer2.groupby(['time', 'date']).sum()
    summer3 = gbDate.loc['2016-06-01':'2016-08-30', ['use', 'gen']]
    summer3 = summer3.groupby(['time', 'date']).sum()
    
    hours = set()
    count = 0
    for row in gbDate.iterrows():
        hours.add(row[0][1])
        if count == 24:
            break;
        count += 1
    hours = list(hours)
    hours.sort()
    
#    temp = summer2.loc['13:00:00'].index
#    temp = [x[5:] for x in temp]
    temp = summer1.index.levels[1].append(summer2.index.levels[1].append(summer3.index.levels[1]))
    summedvals = pd.DataFrame(index = hours, columns = temp)
    summedvals.fillna(0, inplace = True)
    
    pdfvals = pd.DataFrame()
    maxUseOrGen = max(gbDate['gen'].max(), gbDate['use'].max())
    evenspaced = np.arange(0, maxUseOrGen + 1, 1)
    pdfvals['power'] = evenspaced
    
    for hour, k in zip(hours, range(24)):
        plt.figure(figsize=(12,8)) 
        x1 = summer1.loc[hour]['use']
        x2 = summer2.loc[hour]['use']
        x3 = summer3.loc[hour]['use']
        for date in x1.index:
            #fill in the dataframe with the sum of each of the three winters (at corresponding date and time)
            summedvals[date][hour] += x1[date]
        for date in x2.index:
            summedvals[date][hour] += x2[date]
        for date in x3.index:
            summedvals[date][hour] += x3[date]
        combined = x1.append(x2).append(x3)
        kde = stats.gaussian_kde(combined, 0.35)
        pdf = kde.pdf(evenspaced)
        pdfvals[str(k) + ':00 pdf'] = pdf
        plt.axvline(np.percentile(combined, 95), linestyle = '--', color = 'r')
        plt.plot(evenspaced, pdf)
        plt.hist(combined, normed = True)
        plt.ylabel('Probability Density')
        plt.title('Summer Load Histogram for ' + str(k) + ':00')
    
    pdfvals.to_csv('threesummeruse.csv')
    summedvals.T.to_csv('threesummerusesummed.csv')

finaltime = current_milli_time()
print('time taken in milliseconds: ' + str(finaltime-initialtime))