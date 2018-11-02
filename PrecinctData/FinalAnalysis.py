#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 22:38:18 2018

Final analysis script!

@author: Jacob
"""

#Importing libraries
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RidgeCV

#Importing data
df = pd.read_csv('FinalDataLong.csv',encoding = 'utf8')

#Lets take only interesting columns
df.drop(['White', 
         'Black or African American',
         'American Indian and Alaska Native', 
         'Asian',
         'Native Hawaiian and Other Pacific Islander', 
         'Some other race',
         'Two or more races', 
         'Hispanic or Latino (of any race)',
         'Votes', 
         'Votes_R', 
         'Votes_DFL'],inplace = True, axis = 1)
df = pd.get_dummies(df)

#Variable importances
X_train = df.drop(['Turnout','Turnout_R','Turnout_DFL'],axis=1)
y_train = df['Turnout']

#Running a random forest for variable importance
rf = RandomForestRegressor(n_estimators = 1000,
                             n_jobs = -1,
                             max_features = 'sqrt',
                             random_state = 123)
rf.fit(X_train, y_train)

#Showing variable importances
pd.Series(rf.feature_importances_, index = X_train.columns.tolist()).sort_values(ascending = False)

#Lets look at ridge coefficients
ridge = RidgeCV(cv = 5)
ridge.fit(X_train, y_train)
coefs = pd.Series(ridge.coef_, index = X_train.columns.tolist()).sort_values(ascending = False).to_frame()
coefs['abs'] = coefs[0].abs()
coefs.sort_values('abs', ascending = False).drop('abs', axis=1).round(3)