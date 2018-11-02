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

#Now merging with educational data
df_educ = pd.read_csv('FinalEducationData2016.csv')
df_educ.columns = ['County']+[x.replace('Percent; Estimate; Population 25 years and over - ','Prop ') for x in df_educ.drop(['Geography'],axis=1).columns.tolist()]
for i in df_educ.drop(['County'],axis=1).columns.tolist():
    df_educ[i] = df_educ[i]/100
df = df.merge(df_educ, left_on = 'COUNTYNAME', right_on='County')
df.drop(['County'],axis=1,inplace=True)

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
df['MalePop'] = np.where(df['Year']=='2010',df['Male2010'],
                 np.where(df['Year']=='2012',df['Male2012'],
                np.where(df['Year']=='2014',df['Male2014'],df['Male2016'])))
df['FemalePop'] = np.where(df['Year']=='2010',df['Female2010'],
                 np.where(df['Year']=='2012',df['Female2012'],
                np.where(df['Year']=='2014',df['Female2014'],df['Female2016'])))
df['FemaleProp'] = np.where(df['Year']=='2010',df['2010FemaleProp'],
                   np.where(df['Year']=='2012',df['2012FemaleProp'],
                   np.where(df['Year']=='2014',df['2014FemaleProp'],df['2016FemaleProp'])))
df['MillenialProp'] = np.where(df['Year']=='2010',df['2010MilProp'],
                   np.where(df['Year']=='2012',df['2012MilProp'],
                   np.where(df['Year']=='2014',df['2014MilProp'],df['2016MilProp'])))
df['GenXProp'] = np.where(df['Year']=='2010',df['2010GenXProp'],
                   np.where(df['Year']=='2012',df['2012GenXProp'],
                   np.where(df['Year']=='2014',df['2014GenXProp'],df['2016GenXProp'])))
df['BoomerProp'] = np.where(df['Year']=='2010',df['2010BoomerProp'],
                   np.where(df['Year']=='2012',df['2012BoomerProp'],
                   np.where(df['Year']=='2014',df['2014BoomerProp'],df['2016BoomerProp'])))
df['SilentProp'] = np.where(df['Year']=='2010',df['2010SilentProp'],
                   np.where(df['Year']=='2012',df['2012SilentProp'],
                   np.where(df['Year']=='2014',df['2014SilentProp'],df['2016SilentProp'])))
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
         '2016FemaleProp',
         'Male2010', 
         'Female2010', 
         'Male2012', 
         'Female2012',
         'Male2014', 
         'Female2014', 
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
         '2016Silent',
         '2010MilProp',
         '2012MilProp',
         '2014MilProp',
         '2016MilProp',
         '2010GenXProp',
         '2012GenXProp',
         '2014GenXProp',
         '2016GenXProp',
         '2010BoomerProp',
         '2012BoomerProp',
         '2014BoomerProp',
         '2016BoomerProp',
         '2010SilentProp',
         '2012SilentProp',
         '2014SilentProp',
         '2016SilentProp'],axis = 1, inplace = True)
df['Midterms'] = np.where(df['Year'].isin(['2010','2014']),1,0)
df['Year'] = df['Year'].astype('int')
df.drop(['Total population'], axis=1).to_csv('FinalDataLong.csv',encoding='utf8',index=False)

#Lets get Minnesota level data
df.drop(['COUNTYNAME',
         'Turnout',
         'Turnout_R',
         'Turnout_DFL',
         'FemaleProp',
         'Midterms',
         'Proportion White', 
         'Proportion Black or African American',
         'Proportion American Indian and Alaska Native', 
         'Proportion Asian',
         'Proportion Native Hawaiian and Other Pacific Islander',
         'Proportion Some other race', 
         'Proportion Two or more races',
         'Proportion Hispanic or Latino (of any race)'],axis=1,inplace=True)
df = df.groupby('Year').sum()
df['White_Prop'] = df['White']/df['Total population']
df['Black or African American_Prop'] = df['Black or African American']/df['Total population']
df['American Indian and Alaska Native_Prop'] = df['American Indian and Alaska Native']/df['Total population']
df['Asian_Prop'] = df['Asian']/df['Total population']
df['Native Hawaiian and Other Pacific Islander_Prop'] = df['Native Hawaiian and Other Pacific Islander']/df['Total population']
df['Some other race_Prop'] = df['Some other race']/df['Total population']
df['Two or more races_Prop'] = df['Two or more races']/df['Total population']
df['Hispanic or Latino (of any race)_Prop'] = df['Hispanic or Latino (of any race)']/df['Total population']
df['Turnout'] = df['Votes']/df['TotalPop']
df['Turnout_R'] = df['Votes_R']/df['TotalPop']
df['Turnout_DFL'] = df['Votes_DFL']/df['TotalPop']
df['FemaleProp'] = df['FemalePop']/df['TotalPop']
df.drop(['Total population', 'White', 'Black or African American',
       'American Indian and Alaska Native', 'Asian',
       'Native Hawaiian and Other Pacific Islander', 'Some other race',
       'Two or more races', 'Hispanic or Latino (of any race)','TotalPop', 'MalePop', 'FemalePop','Votes','Votes_R','Votes_DFL'],axis=1,inplace=True)
df.to_csv('MNbyYear.csv')
