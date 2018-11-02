#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 14:57:35 2018

This script creates the congression district population data

@author: Jacob
"""

#importing packages
import pandas as pd
import numpy as np

#Importing data
#2010
df2010 = pd.read_csv('CongPop2010.csv',skiprows=1)
df2010 = df2010[['Total; Estimate; Total population',
                 'Total; Estimate; SELECTED AGE CATEGORIES - 18 years and over']]
df2010.columns = ['TotalPop','PercentOver18']
df2010['VotingPop2010'] = np.round(df2010['TotalPop']*(df2010['PercentOver18']/100)).astype('int')
df2010.drop(['TotalPop','PercentOver18'],axis=1,inplace=True)
df2010.index = [1,2,3,4,5,6,7,8]

#2012
df2012 = pd.read_csv('CongPop2012.csv',skiprows=1)
df2012 = df2012[['Total; Estimate; Total population',
                 'Total; Estimate; SELECTED AGE CATEGORIES - 18 years and over']]
df2012.columns = ['TotalPop','PercentOver18']
df2012['VotingPop2012'] = np.round(df2012['TotalPop']*(df2012['PercentOver18']/100)).astype('int')
df2012.drop(['TotalPop','PercentOver18'],axis=1,inplace=True)
df2012.index = [1,2,3,4,5,6,7,8]

#2014
df2014 = pd.read_csv('CongPop2014.csv',skiprows=1)
df2014 = df2014[['Total; Estimate; Total population',
                 'Total; Estimate; SELECTED AGE CATEGORIES - 18 years and over']]
df2014.columns = ['TotalPop','PercentOver18']
df2014['VotingPop2014'] = np.round(df2014['TotalPop']*(df2014['PercentOver18']/100)).astype('int')
df2014.drop(['TotalPop','PercentOver18'],axis=1,inplace=True)
df2014.index = [1,2,3,4,5,6,7,8]

#2016
df2016 = pd.read_csv('CongPop2016.csv',skiprows=1)
df2016 = df2016[['Total; Estimate; Total population',
                 'Total; Estimate; SELECTED AGE CATEGORIES - 18 years and over']]
df2016.columns = ['TotalPop','PercentOver18']
df2016['VotingPop2016'] = np.round(df2016['TotalPop']*(df2016['PercentOver18']/100)).astype('int')
df2016.drop(['TotalPop','PercentOver18'],axis=1,inplace=True)
df2016.index = [1,2,3,4,5,6,7,8]

#Creating wide data
df = df2010.merge(df2012,right_index=True,left_index=True).merge(df2014,right_index=True,left_index=True).merge(df2016,right_index=True,left_index=True)
df.to_csv('CongPopsWide.csv')

#Creating long data
df_long = df.melt(value_vars = ['VotingPop2010','VotingPop2012','VotingPop2014','VotingPop2016'],
                  var_name = 'Year',
                  value_name = 'VotingPop')
df_long['Year'] = [x.replace('VotingPop','') for x in df_long['Year']]
df_long['Year'] = df_long['Year'].astype('int')
df_long['District'] = [1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8]
df_long.to_csv('CongPopsLong.csv',index=False)
