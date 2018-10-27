#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 11:02:34 2018

This script takes population estimates for the counties

@author: Jacob
"""

#Loading packages
import pandas as pd

#Loading in our csv
df = pd.read_csv('PEP_2017_PEPAGESEX_with_ann.csv')
df = df.drop(df.index[0])

#Lets only pull off selected columns
df = df[['GEO.display-label',
         'est72010sex0_age18plus',
         'est72010sex1_age18plus',
         'est72010sex2_age18plus',
         'est72012sex0_age18plus',
         'est72012sex1_age18plus',
         'est72012sex2_age18plus',
         'est72014sex0_age18plus',
         'est72014sex1_age18plus',
         'est72014sex2_age18plus',
         'est72016sex0_age18plus',
         'est72016sex1_age18plus',
         'est72016sex2_age18plus']]

#Changing columns names
df.columns = ['County',
              'Total2010',
              'Male2010',
              'Female2010',
              'Total2012',
              'Male2012',
              'Female2012',
              'Total2014',
              'Male2014',
              'Female2014',
              'Total2016',
              'Male2016',
              'Female2016']

#Coercing to int
for i in ['Total2010',
              'Male2010',
              'Female2010',
              'Total2012',
              'Male2012',
              'Female2012',
              'Total2014',
              'Male2014',
              'Female2014',
              'Total2016',
              'Male2016',
              'Female2016']:
    df[i] = df[i].astype('int')

#Lets create proportion columns
df['2010FemaleProp'] = df['Female2010']/df['Total2010']
df['2012FemaleProp'] = df['Female2012']/df['Total2012']
df['2014FemaleProp'] = df['Female2014']/df['Total2014']
df['2016FemaleProp'] = df['Female2016']/df['Total2016']

#Lets snip off the last x characters of the County
df['County'] = [x.replace(' County, Minnesota','') for x in df['County'].tolist()]

#Lets save this
df.to_csv('PopulationData.csv', index = False)
