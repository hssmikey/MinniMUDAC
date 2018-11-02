#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 11:39:55 2018

This script integrates our county-level data into 1 csv

@author: Jacob
"""

#Loading libraries
import pandas as pd

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

#Saving the final data to a CSV
df.to_csv('FinalData.csv', index = False)