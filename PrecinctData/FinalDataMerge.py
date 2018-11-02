#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 11:39:55 2018

This script integrates our county-level data into 1 csv

@author: Jacob
"""

#Loading libraries
import pandas as pd
import numpy as np

#Loading our datasets
df_votes = pd.read_csv('VotesByCountyByYear.csv')
df_pop = pd.read_csv('PopulationData.csv')

#Lets do a merge
df = df_votes.merge(df_pop, left_on = 'COUNTYNAME', right_on = 'County')

#Lets create our turnout rates
#Overall
df['2010Turnout'] = df['2010Votes']/df['Total2010']
df['2012Turnout'] = df['2012Votes']/df['Total2012']
df['2014Turnout'] = df['2014Votes']/df['Total2014']
df['2016Turnout'] = df['2016Votes']/df['Total2016']
#Republican
df['2010Turnout_R'] = df['2010Votes_R']/df['Total2010']
df['2012Turnout_R'] = df['2012Votes_R']/df['Total2012']
df['2014Turnout_R'] = df['2014Votes_R']/df['Total2014']
df['2016Turnout_R'] = df['2016Votes_R']/df['Total2016']
#DFL
df['2010Turnout_DFL'] = df['2010Votes_DFL']/df['Total2010']
df['2012Turnout_DFL'] = df['2012Votes_DFL']/df['Total2012']
df['2014Turnout_DFL'] = df['2014Votes_DFL']/df['Total2014']
df['2016Turnout_DFL'] = df['2016Votes_DFL']/df['Total2016']

#Now we have to merge with demographic data
df_demo = pd.read_csv('Final2016DemographicData.csv', encoding = 'utf8')
df = df.merge(df_demo, left_on = 'COUNTYNAME', right_on = 'County')
df.drop(['County_x','County_y','2010Votes_Total','2012Votes_Total','2014Votes_Total','2016Votes_Total'], axis = 1, inplace = True)

#Saving the final data to a CSV
df.to_csv('FinalData.csv', index = False)

#Lets create a long form
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
df['Votes'] = np.where(df['Year']=='2010',df['2010Votes'],
              np.where(df['Year']=='2012',df['2012Votes'],
              np.where(df['Year']=='2014',df['2014Votes'],df['2016Votes'])))
df['Votes_R'] = np.where(df['Year']=='2010',df['2010Votes_R'],
              np.where(df['Year']=='2012',df['2012Votes_R'],
              np.where(df['Year']=='2014',df['2014Votes_R'],df['2016Votes_R'])))
df['Votes_DFL'] = np.where(df['Year']=='2010',df['2010Votes_DFL'],
              np.where(df['Year']=='2012',df['2012Votes_DFL'],
              np.where(df['Year']=='2014',df['2014Votes_DFL'],df['2016Votes_DFL'])))
df['Turnout_R'] = np.where(df['Year']=='2010',df['2010Turnout_R'],
              np.where(df['Year']=='2012',df['2012Turnout_R'],
              np.where(df['Year']=='2014',df['2014Turnout_R'],df['2016Turnout_R'])))
df['Turnout_DFL'] = np.where(df['Year']=='2010',df['2010Turnout_DFL'],
              np.where(df['Year']=='2012',df['2012Turnout_DFL'],
              np.where(df['Year']=='2014',df['2014Turnout_DFL'],df['2016Turnout_DFL'])))
df['TotalPop'] = np.where(df['Year']=='2010',df['Total2010'],
                 np.where(df['Year']=='2012',df['Total2012'],
                np.where(df['Year']=='2014',df['Total2014'],df['Total2016'])))
df['FemaleProp'] = np.where(df['Year']=='2010',df['2010FemaleProp'],
                   np.where(df['Year']=='2012',df['2012FemaleProp'],
                   np.where(df['Year']=='2014',df['2014FemaleProp'],df['2016FemaleProp'])))
df.drop(['Total2010',
         'Total2012',
         'Total2014',
         'Total2016',
         '2010Votes',
         '2012Votes',
         '2014Votes',
         '2016Votes',
         '2010Votes_R',
         '2012Votes_R',
         '2014Votes_R',
         '2016Votes_R',
         '2010Votes_DFL',
         '2012Votes_DFL',
         '2014Votes_DFL',
         '2016Votes_DFL',
         '2010Turnout_R',
         '2012Turnout_R',
         '2014Turnout_R',
         '2016Turnout_R',
         '2010Turnout_DFL',
         '2012Turnout_DFL',
         '2014Turnout_DFL',
         '2016Turnout_DFL',
         '2010FemaleProp',
         '2012FemaleProp',
         '2014FemaleProp',
         '2016FemaleProp'],axis = 1, inplace = True)
df['Midterms'] = np.where(df['Year'].isin(['2010','2014']),1,0)
df['Year'] = df['Year'].astype('int')
df.to_csv('FinalDataLong.csv',encoding='utf8',index=False)