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
from sklearn.linear_model import RidgeCV, LinearRegression,Ridge
import seaborn as sns
import matplotlib.pyplot as plt

#Importing data
df = pd.read_csv('FinalDataLong.csv',encoding = 'utf8')
df_backup = df
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

#We need to log totalpo
X_train['TotalPop'] = np.log(X_train['TotalPop'])

#Univariate Analysis
#Demographic Proportions
for i in [x for x in X_train.columns.tolist() if not x.startswith('COUNTYNAME_')]:
    print(i)
    print(X_train[i].hist(bins=30))
    plt.show()

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
ridge.intercept_
coefs[~coefs['index'].str.startswith('COUNTYNAME_')].set_index('index')

#Lets try a logit model which may be better
import statsmodels.api as sm
X_train = sm.add_constant(X_train)
binomial_model = sm.GLM(y_train, X_train, family=sm.families.Binomial())
binomial_results = binomial_model.fit()
binomial_results.summary()

#What would our predictions look like?
binomial_results.predict(X_train)

#Lets just see an array
df_sub = df[[x for x in df.columns.tolist() if not x.startswith('COUNTYNAME_')]]
df_sub_corr = df_sub.corr()[['Turnout','Turnout_R','Turnout_DFL']]
#df_sub_corr.index = [x.replace('Proportion','Prop')[0:12] for x in df_sub_corr.index.tolist()]
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
df_sub_corr.to_csv('ImportantCorrelations.csv')

###############################################################################
#Time for creating the actual predictions
###############################################################################
#We want first:
#County-level
#Midterm:1
#Year:2018
#Use 2016 Demographic data
#We need to forecast total population for each county

#We will use our RF from earlier

#Importing data
df = pd.read_csv('FinalDataLong.csv',encoding = 'utf8')
df_backup = df
#Lets take only interesting columns
df.drop(['White', 
         'Black or African American',
         'American Indian and Alaska Native', 
         'Asian',
         'Native Hawaiian and Other Pacific Islander', 
         'Some other race',
         'Two or more races', 
         'Hispanic or Latino (of any race)', 
         'Votes_R', 
         'Votes_DFL',
         'Turnout',
         'Turnout_R',
         'Turnout_DFL',
         'FemalePop',
         'MalePop'],inplace = True, axis = 1)
df = pd.get_dummies(df)

#Variable importances
X_train = df.drop(['Votes'],axis=1)
y_train = df['Votes']

#Lets log votes
y_train = np.log(y_train)

#We need to log totalpop
X_train['TotalPop'] = np.log(X_train['TotalPop'])

#Creating our new prediction data
X_test = X_train[X_train['Year']==2016]
X_test.reset_index(inplace=True)
X_test.drop(['index'],axis=1,inplace=True)
X_test['Year'] = 2018
X_test['Midterms'] = 1

#Now we need to adjust for population changes
X_pop = X_train.drop(['TotalPop'],axis=1)
y_pop = X_train['TotalPop']

#Fitting a linear trend for this
forecasts = []
for i in [x for x in X_train.columns if x.startswith('COUNTYNAME_')]:
    df_forecast = X_train[X_train[i]==1]
    X_forecast = df_forecast['Year'].values.reshape(-1,1)
    y_forecast = df_forecast['TotalPop']
    model = LinearRegression()
    model.fit(X_forecast,y_forecast)
    forecasts.append(model.predict(np.array([2018]).reshape(-1,1)).tolist()[0])
pd.DataFrame({'2010':X_train[X_train['Year']==2010]['TotalPop'].tolist(),
              '2012':X_train[X_train['Year']==2012]['TotalPop'].tolist(),
              '2014':X_train[X_train['Year']==2014]['TotalPop'].tolist(),
              '2016':X_train[X_train['Year']==2016]['TotalPop'].tolist(),
              '2018':forecasts})

#Imputing new population values
X_test['TotalPop'] = forecasts

#Fitting a tuned random forest for prediction
from sklearn.model_selection import GridSearchCV
params = {'n_estimators':[1000],
          'max_features':[None]}
rf = RandomForestRegressor(n_jobs = -1,random_state = 123)
gs = GridSearchCV(rf, params, cv=5,verbose=2)
gs.fit(X_train, y_train)
gs.best_params_

#Lets predict
count_preds = np.exp(gs.predict(X_test)).astype('int')
count_preds

#Lets compare over time
df_turnout = pd.read_csv('FinalData.csv')
df_turnout = df_turnout[['COUNTYNAME','2010Votes','2012Votes','2014Votes','2016Votes']]
df_turnout['2018Prediction'] = count_preds
df_turnout.to_csv('Predictions.csv', index = False)

#Now we need to convert this to congressional levels
district1 = ['Blue Earth','Brown','Cottonwood','Dodge','Faribault','Fillmore','Freeborn','Houston','Jackson','Le Sueur','Martin','Mower','Nicollet','Nobles','Olmsted','Rice','Rock','Steele','Waseca','Watonwan','Winona']
district2 = ['Dakota','Goodhue','Rice','Scott','Wabasha','Washington']
district3 = ['Anoka','Carver','Hennepin']
district4 = ['Ramsey','Washington']
district5 = ['Anoka','Ramsey']
district6 = ['Anoka','Benton','Carver','Hennepin','Sherburne','Stearns','Washington','Wright']
district7 = ['Becker','Beltrami','Big Stone','Chippewa','Clay','Clearwater','Cottonwood','Douglas','Grant','Kandiyohi','Kittson','Lac qui Parle','Lake of the Woods','Lincoln','Lyon','McLeod','Mahnomen','Marshall','Meeker','Murray','Norman','Otter Tail','Pennington','Pipestone','Polk','Pope','Red Lake','Redwood','Renville','Roseau','Sibley','Stearns','Stevens','Swift','Todd','Traverse','Wilkin','Yellow Medicine']
district8 = ['Aitkin','Beltrami','Carlton','Cass','Chisago','Cook','Crow Wing','Hubbard','Isanti','Itasca','Kanabec','Koochiching','Lake','Mille Lacs','Morrison','Pine','St. Louis','Wadena']

#Pulling in our congressional data
df_cong = pd.read_csv('CongressionalVoteTotals.csv')

#Making sure all counties are spelled correctly
real_names = df_cong.drop(['Year','Votes','District'],axis=1).columns.tolist()
our_names = list(set(district1+district2+district3+district4+district5+district6+district7+district8))
len(real_names)-len(our_names)
[print(x) for x in our_names if x not in real_names]
[print(x) for x in real_names if x not in our_names]
#We are good!

#Which districts have split counties?
b = {}
for item in district1+district2+district3+district4+district5+district6+district7+district8:
    b[item] = b.get(item, 0) + 1
b = dict((k, v) for k, v in b.items() if v > 1)
list(b.keys())
#All districts have split counties
district_counts = [district1,district2,district3,district4,district5,district6,district7,district8]
estimator_list = []
for i in [1,2,3,4,5,6,7,8]:
    district_df = df_cong[(df_cong['District']==i)&(df_cong['Year'].isin([2014,2016]))]
    district_df = district_df[['Votes']+district_counts[i-1]]
    unique_counties = [x for x in district_counts[i-1] if x not in list(b.keys())]
    reduc_df = district_df
    for j in unique_counties:
        reduc_df['Votes'] = reduc_df['Votes']-reduc_df[j]
        reduc_df.drop([j],axis=1,inplace=True)
    y = reduc_df['Votes']
    x = reduc_df.drop(['Votes'],axis=1)
    model = LinearRegression(fit_intercept=False).fit(x,y)
    weights = dict(zip(x.columns.tolist(),model.coef_))
    final_weights = []
    for j in range(len(district_counts[i-1])):
        if district_counts[i-1][j] not in list(b.keys()):
            final_weights.append(1)
        else:
            final_weights.append(weights[district_counts[i-1][j]])
    estimator_list.append(dict(zip(district_counts[i-1],final_weights)))

predictions = pd.Series(count_preds, index = real_names)
final_predictions = []
for i in [1,2,3,4,5,6,7,8]:
    subbed = predictions[list(estimator_list[i-1].keys())]
    final_predictions.append(int(sum([a*b for a,b in zip(subbed.values,list(estimator_list[i-1].values()))])))
final_predictions

#Lets compare this to District totals
df_final = pd.read_csv('CongressionalVoteTotalsWide.csv')
df_final['2018preds'] = final_predictions
df_final.to_csv('FinalCongressionalPredictions.csv',index=False)