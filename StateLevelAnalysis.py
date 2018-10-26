#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 19:19:25 2018

This file is the state-level analysis of voting habits for MN

@author: Jacob
"""

#Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Importing our data
df = pd.read_excel('minnesota-election-statistics-1950-to-2016.xlsx', skiprows = 1, sheetname = 1)
df.drop(df.tail(1).index,inplace=True)

#Lets create a election type indicator
df['Presidential'] = np.where(df['Year']%4>0,0,1)
df['YearSince1950'] = df['Year']-1950

#Lets see a run-sequence plot
plt.plot(df[df['Presidential']==1]['Year'],df[df['Presidential']==1]['Percent Turnout'], label = 'Presidental Elections')
plt.plot(df[df['Presidential']==0]['Year'],df[df['Presidential']==0]['Percent Turnout'], label = 'Midterm Elections')
plt.xlabel('Year')
plt.ylabel('Turnout Rate')
plt.title('MN Voter Turnout Rate by Year')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

#Lets try a regular linear regression
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(df[['YearSince1950','Presidential']],df['Percent Turnout'])
print("Coefficients: ", model.coef_.round(5), " Intercept: ", round(model.intercept_,5))

#Lets do this with a LassoCV
from sklearn.linear_model import LassoCV
model = LassoCV()
model.fit(df[['YearSince1950','Presidential']],df['Percent Turnout'])
print("Coefficients: ", model.coef_.round(5), " Intercept: ", round(model.intercept_,5))

#Okay, now lets test for autocorrelation
from pandas.plotting import autocorrelation_plot
autocorrelation_plot(df['Percent Turnout'])
#Looks like there is at least 2nd-3rd order autocorrelation on a statewide basis

#Lets try an auto-arima
from pyramid.arima import auto_arima
stepwise_fit = auto_arima(df['Percent Turnout'].values, 
                          start_p=1, 
                          start_q=0, 
                          max_p=5, 
                          max_q=0, 
                          test = 'kpss',
                          max_d = 2,
                          seasonal = True,
                          m=2,
                          error_action='ignore',
                          suppress_warnings=True,
                          stepwise=False,
                          ic = 'bic')
stepwise_fit.summary()
#It seems like this is a 3rd order 
#We could probably just model it as a 1st/2nd order due to low number of observations

#Lets just fit a second order model
import pyramid as pm
arima_model = pm.ARIMA(order=(2,0,0))
arima_model.fit(df['Percent Turnout'].values)
arima_model.summary()
