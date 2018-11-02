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
         'Votes_DFL',
         'FemalePop',
         'MalePop'],inplace = True, axis = 1)
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

#Lets test for normality first
y_train.hist(bins = 20)
#Bimodal distribution show that linear regression is definitely not appropriate

#Lets look at ridge coefficients
ridge = RidgeCV(np.linspace(0,10,50),cv = 10)
ridge.fit(X_train, y_train)
ridge.alpha_
coefs = pd.Series(ridge.coef_, index = X_train.columns.tolist()).sort_values(ascending = False).to_frame()
coefs['abs'] = coefs[0].abs()
coefs = coefs.sort_values('abs', ascending = False).drop('abs', axis=1).round(4)

#Lets drop countynames
coefs.reset_index(inplace=True)
coefs[~coefs['index'].str.startswith('COUNTYNAME_')].set_index('index')

#Lets try a logit model which may be better
import statsmodels.api as sm
X_train = sm.add_constant(X_train)
binomial_model = sm.GLM(y_train, X_train, family=sm.families.Binomial())
binomial_results = binomial_model.fit()
binomial_results.summary()

#What would our predictions look like?
binomial_results.predict(X_train)

#Correlation heatmap
import seaborn as sns
import matplotlib.pyplot as plt
def halfHeatMap(df, mirror):
    # Create Correlation df
    corr = df.corr()
    # Plot figsize
    fig, ax = plt.subplots(figsize=(10, 10))
    # Generate Color Map
    colormap = sns.diverging_palette(220, 10, as_cmap=True)

    if mirror == True:
        #Generate Heat Map, allow annotations and place floats in map
        sns.heatmap(corr, cmap=colormap, annot=True, fmt=".2f")
        #Apply xticks
        plt.xticks(range(len(corr.columns)), corr.columns);
        #Apply yticks
        plt.yticks(range(len(corr.columns)), corr.columns)
        #show plot
        plt.show()
    else:
        # Drop self-correlations
        dropSelf = np.zeros_like(corr)
        dropSelf[np.triu_indices_from(dropSelf)] = True# Generate Color Map
        colormap = sns.diverging_palette(220, 10, as_cmap=True)
        # Generate Heat Map, allow annotations and place floats in map
        sns.heatmap(corr, cmap=colormap, annot=True, fmt=".2f", mask=dropSelf)
        # Apply xticks
        plt.xticks(range(len(corr.columns)), corr.columns);
        # Apply yticks
        plt.yticks(range(len(corr.columns)), corr.columns)
        #show plot
        plt.show()
df_sub = df[[x for x in df.columns.tolist() if not x.startswith('COUNTYNAME_')]]
halfHeatMap(df_sub, mirror = False)

#Lets just see an array
df_sub_corr = df_sub.corr()[['Turnout','Turnout_R','Turnout_DFL']]
df_sub_corr.index = [x.replace('Proportion','Prop')[0:12] for x in df_sub_corr.index.tolist()]
df_sub_corr
fig, ax = plt.subplots(figsize=(10, 10))
colormap = sns.diverging_palette(220, 10, as_cmap=True)
# Generate Heat Map, allow annotations and place floats in map
sns.heatmap(df_sub_corr, cmap=colormap, annot=True, fmt=".2f")
# Apply xticks
plt.xticks(range(len(df_sub_corr.columns)), df_sub_corr.columns);
# Apply yticks
plt.yticks(range(len(df_sub_corr.index)), df_sub_corr.index)
#show plot
plt.show()