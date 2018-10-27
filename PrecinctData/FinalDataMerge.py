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
df['2010Turnout'] = df['2010Votes']/df['Total2010']
df['2012Turnout'] = df['2012Votes']/df['Total2012']
df['2014Turnout'] = df['2014Votes']/df['Total2014']
df['2016Turnout'] = df['2016Votes']/df['Total2016']

#Saving the final data to a CSV
df.to_csv('FinalData.csv')