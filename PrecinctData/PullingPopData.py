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
df.columns = df.columns.to_series().apply(lambda x: x.strip())

#Lets get the list of our age columns
#AgeRange columns (14 elements)
age_cols = [x for x in df.columns.tolist() if x.endswith('sex0_age20to24') or x.endswith('sex0_age25to29') or x.endswith('sex0_age30to34')  or x.endswith('sex0_age35to39') or x.endswith('sex0_age40to44')  or x.endswith('sex0_age45to49') or x.endswith('sex0_age50to54')  or x.endswith('sex0_age55to59') or x.endswith('sex0_age60to64')  or x.endswith('sex0_age65to69') or x.endswith('sex0_age70to74')  or x.endswith('sex0_age75to79') or x.endswith('sex0_age80to84')  or x.endswith('sex0_age85plus')]
age_cols = [x for x in age_cols if x.startswith('est7')]
age_cols = [x for x in age_cols if '2010' in x or '2012' in x or '2014' in x or '2016' in x]

#Over 18 cols
over18_cols = [x for x in df.columns.tolist() if x.endswith('age18plus')]
over18_cols = [x for x in over18_cols if x.startswith('est7')]
over18_cols = [x for x in over18_cols if '2010' in x or '2012' in x or '2014' in x or '2016' in x]

#Lets only pull off selected columns
columns_list = ['GEO.display-label']+age_cols+over18_cols
df = df[columns_list]

#Creating our 3 age groups
#Millenial
df['2010Millenial'] = df['est72010sex0_age20to24']+df['est72010sex0_age25to29']+df['est72010sex0_age30to34']
df['2012Millenial'] = df['est72012sex0_age20to24']+df['est72012sex0_age25to29']+df['est72012sex0_age30to34']
df['2014Millenial'] = df['est72014sex0_age20to24']+df['est72014sex0_age25to29']+df['est72014sex0_age30to34']
df['2016Millenial'] = df['est72016sex0_age20to24']+df['est72016sex0_age25to29']+df['est72016sex0_age30to34']
#GenX
df['2010GenX'] = df['est72010sex0_age35to39']+df['est72010sex0_age40to44']+df['est72010sex0_age45to49']
df['2012GenX'] = df['est72012sex0_age35to39']+df['est72012sex0_age40to44']+df['est72012sex0_age45to49']
df['2014GenX'] = df['est72014sex0_age35to39']+df['est72014sex0_age40to44']+df['est72014sex0_age45to49']
df['2016GenX'] = df['est72016sex0_age35to39']+df['est72016sex0_age40to44']+df['est72016sex0_age45to49']
#Boomer
df['2010Boomer'] = df['est72010sex0_age50to54']+df['est72010sex0_age55to59']+df['est72010sex0_age60to64']+df['est72010sex0_age65to69']
df['2012Boomer'] = df['est72012sex0_age50to54']+df['est72012sex0_age55to59']+df['est72012sex0_age60to64']+df['est72012sex0_age65to69']
df['2014Boomer'] = df['est72014sex0_age50to54']+df['est72014sex0_age55to59']+df['est72014sex0_age60to64']+df['est72014sex0_age65to69']
df['2016Boomer'] = df['est72016sex0_age50to54']+df['est72016sex0_age55to59']+df['est72016sex0_age60to64']+df['est72016sex0_age65to69']
#Silent
df['2010Silent'] = df['est72010sex0_age70to74']+df['est72010sex0_age75to79']+df['est72010sex0_age80to84']+df['est72010sex0_age85plus']
df['2012Silent'] = df['est72012sex0_age70to74']+df['est72012sex0_age75to79']+df['est72012sex0_age80to84']+df['est72012sex0_age85plus']
df['2014Silent'] = df['est72014sex0_age70to74']+df['est72014sex0_age75to79']+df['est72014sex0_age80to84']+df['est72014sex0_age85plus']
df['2016Silent'] = df['est72016sex0_age70to74']+df['est72016sex0_age75to79']+df['est72016sex0_age80to84']+df['est72016sex0_age85plus']

#Dropping original columns
df.drop(age_cols,axis = 1,inplace=True)

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
              'Female2016', 
              '2010Millenial',
              '2012Millenial', 
              '2014Millenial', 
              '2016Millenial', 
              '2010GenX',
              '2012GenX', 
              '2014GenX', 
              '2016GenX', 
              '2010Boomer', 
              '2012Boomer',
              '2014Boomer', 
              '2016Boomer', 
              '2010Silent', 
              '2012Silent', 
              '2014Silent',
              '2016Silent']

#Coercing to int
for i in df.columns.tolist()[1:]:
    df[i] = df[i].astype('int')

#Lets create proportion columns
df['2010FemaleProp'] = df['Female2010']/df['Total2010']
df['2012FemaleProp'] = df['Female2012']/df['Total2012']
df['2014FemaleProp'] = df['Female2014']/df['Total2014']
df['2016FemaleProp'] = df['Female2016']/df['Total2016']

df['2010MilProp'] = df['2010Millenial']/df['Total2010']
df['2012MilProp'] = df['2012Millenial']/df['Total2012']
df['2014MilProp'] = df['2014Millenial']/df['Total2014']
df['2016MilProp'] = df['2016Millenial']/df['Total2016']

df['2010GenXProp'] = df['2010GenX']/df['Total2010']
df['2012GenXProp'] = df['2012GenX']/df['Total2012']
df['2014GenXProp'] = df['2014GenX']/df['Total2014']
df['2016GenXProp'] = df['2016GenX']/df['Total2016']

df['2010BoomerProp'] = df['2010Boomer']/df['Total2010']
df['2012BoomerProp'] = df['2012Boomer']/df['Total2012']
df['2014BoomerProp'] = df['2014Boomer']/df['Total2014']
df['2016BoomerProp'] = df['2016Boomer']/df['Total2016']

df['2010SilentProp'] = df['2010Silent']/df['Total2010']
df['2012SilentProp'] = df['2012Silent']/df['Total2012']
df['2014SilentProp'] = df['2014Silent']/df['Total2014']
df['2016SilentProp'] = df['2016Silent']/df['Total2016']

#Lets snip off the last x characters of the County
df['County'] = [x.replace(' County, Minnesota','') for x in df['County'].tolist()]

#Lets save this
df.to_csv('PopulationData.csv', index = False)
