import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

# import data
weather_data = pd.read_csv('loyola_jan2011.txt').set_index('HOUR-PST')

# create hourly irradiance profiles for each day
irradiance = pd.DataFrame(index=range(24))
for day in range(1,32):
    irradiance['1/'+str(day)] = weather_data[weather_data['DATE (MM/DD/YYYY)']=='1/'+str(day)+'/2011']['Avg Global Horizontal [W/m^2]']

# fit beta distribution for a given hour, here we use 1pm
data = irradiance.loc[13]
(a,b,loc,scale)=stats.beta.fit(data,5,5,floc=0,scale=data.max())

# fit PDF to coefficients
x = np.linspace(0,data.max()*1.01,100)
pdf = stats.beta.pdf(x,a,b,loc=loc,scale=scale)

# plot histogram and PDF together
plt.plot(x,pdf)
plt.hist(data,normed=True)
plt.xlabel('Irradiance')
plt.ylabel('Probability Density')