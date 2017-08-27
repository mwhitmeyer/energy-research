# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 18:30:55 2017

@author: whitt
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

threeyears = pd.read_csv('12012013-08312016thirtyhomes.csv')

#get rid of timezone at the end of the localminute obj 
threeyears['localminute'] = [row[1][:len(row[1]) - 3] for row in threeyears.itertuples()] 

threeyears['date'], threeyears['time'] = threeyears['localminute'].str.split(' ', 1).str

threeyears['localminute'] = [pd.to_datetime(row[1]) for row in threeyears.itertuples()]

totalhourly = threeyears.groupby(['time', 'date']).sum()


def getAllWinterData():
    winter1 = threeyears.loc['2013-12-01':'2014-02-28', ['use', 'gen', 'time', 'date']]
    winter2 = threeyears.loc['2014-12-01':'2015-02-28', ['use', 'gen', 'time', 'date']]
    winter3 = threeyears.loc['2015-12-01':'2016-02-28', ['use', 'gen', 'time', 'date']]
    

def getAllSummerData():
    summer1 = threeyears.loc['2014-06-01':'2014-08-30', ['use', 'gen', 'time', 'date']]



