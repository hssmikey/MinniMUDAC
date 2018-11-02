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
df = pd.read_csv('FinalData.csv',encoding = 'utf8')

#Lets take only interesting columns
df = df[['COUNTYNAME',
         '2010Turnout',
         '2012Turnout', 
         '2014Turnout', 
         '2016Turnout',
         'Total2010',
         'Total2012',
         'Total2014',
         'Total2016',
         '2010FemaleProp',
         '2012FemaleProp',
         '2014FemaleProp',
         '2016FemaleProp',
         'Proportion White', 
         'Proportion Black or African American',
         'Proportion American Indian and Alaska Native', 
         'Proportion Asian',
         'Proportion Native Hawaiian and Other Pacific Islander',
         'Proportion Some other race', 
         'Proportion Two or more races',
         'Proportion Hispanic or Latino (of any race)']]

#We need to convert from wide to long format using a year column
df = df.melt(id_vars = df.drop(['2010Turnout',
                        '2012Turnout', 
                        '2014Turnout', 
                        '2016Turnout'],axis = 1).columns.tolist(),
             value_vars = ['2010Turnout',
                        '2012Turnout', 
                        '2014Turnout', 
                        '2016Turnout'],
              var_name = 'Year',
              value_name = 'Turnout')
df['Year'] = [x[0:4] for x in df.Year.tolist()]
df['Total'] = np.where(df['Year']=='2010',df['Total2010'],
              np.where(df['Year']=='2012',df['Total2012'],
              np.where(df['Year']=='2014',df['Total2014'],df['Total2016'])))
df['FemaleProp'] = np.where(df['Year']=='2010',df['2010FemaleProp'],
                   np.where(df['Year']=='2012',df['2012FemaleProp'],
                   np.where(df['Year']=='2014',df['2014FemaleProp'],df['2016FemaleProp'])))
df.drop(['Total2010',
         'Total2012',
         'Total2014',
         'Total2016',
         '2010FemaleProp',
         '2012FemaleProp',
         '2014FemaleProp',
         '2016FemaleProp'],axis = 1, inplace = True)
df['Midterms'] = np.where(df['Year'].isin(['2010','2014']),1,0)
df['Year'] = df['Year'].astype('int')
df = pd.get_dummies(df)

#Variable importances
X_train = df.drop(['Turnout'],axis=1)
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
