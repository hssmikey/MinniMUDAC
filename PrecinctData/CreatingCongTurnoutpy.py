#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 16:16:59 2018

This script creates the congressional dataset

@author: Jacob
"""

#Loading packages
import pandas as pd

#By county
#2010
df2010 = pd.read_excel('2010_general_results_final.xls',sheetname = 0)
df2010 = df2010[['CountyID',
                 'TotVoters',
                 'CONGR',
                 'CONGDFL']]
df2010.columns = ['CountyCode',
                  '2010Votes',
                  '2010Votes_R',
                  '2010Votes_DFL']
df2010 = df2010.groupby(['CountyCode']).sum()

#2012
df2012 = pd.read_excel('2012mngeneralelectionresults_official_postrecounts.xlsx',sheetname = 0)
df2012 = df2012[['COUNTYCODE',
                 'TOTVOTING',
                 'USPRSR',
                 'USPRSDFL']]
df2012.columns = ['CountyCode',
                  '2012Votes',
                  '2012Votes_R',
                  '2012Votes_DFL']
df2012 = df2012.groupby(['CountyCode']).sum()

#2014
df2014 = pd.read_excel('2014-general-federal-state-results-by-precinct-official.xlsx',sheetname = 0)
df2014 = df2014[['COUNTYCODE',
                 'TOTVOTING',
                 'USSENR',
                 'USSENDFL']]
df2014.columns = ['CountyCode',
                  '2014Votes',
                  '2014Votes_R',
                  '2014Votes_DFL']
df2014 = df2014.groupby(['CountyCode']).sum()

#2016
df2016 = pd.read_excel('2016-general-federal-state-results-by-precinct-official.xlsx',sheetname = 0)
df2016 = df2016[['COUNTYCODE',
                 'TOTVOTING',
                 'USPRSR',
                 'USPRSDFL']]
df2016.columns = ['CountyCode',
                  '2016Votes',
                  '2016Votes_R',
                  '2016Votes_DFL']
df2016 = df2016.groupby(['CountyCode']).sum()

#Binding all years together
df = df2010.merge(df2012, left_index=True,right_index=True).merge(df2014, left_index=True,right_index=True).merge(df2016, left_index=True,right_index=True)

#Now we have to sub in county names
county_list = pd.read_excel('2016-general-federal-state-results-by-precinct-official.xlsx',sheetname = 0)
county_list = county_list[['COUNTYNAME','COUNTYCODE']].groupby(['COUNTYCODE']).first()
df = df.merge(county_list, right_index = True, left_index = True)
df = df.set_index('COUNTYNAME')
df = df.transpose()
df.reset_index(level=0, inplace=True)
df['Year'] = [x[0:4] for x in df['index'].tolist()]
df['Year'] = df['Year'].astype('int')
df = df.iloc[[0,3,6,9]]
df.drop(['index'],axis=1,inplace=True)

#We need to convert this to proportions
df_pop = pd.read_csv('PopulationData.csv')
df_pop = df_pop[['County','Total2010','Total2012','Total2014','Total2016']]
df_pop = df_pop.transpose()
df_pop.columns = df_pop.iloc[0]
df_pop = df_pop.reindex(df_pop.index.drop('County'))
df_pop['Year'] = [x[-4:] for x in df_pop.index.tolist()]

#Lets merge them
df.set_index(['Year'],inplace=True)
df_pop.set_index(['Year'],inplace=True)
for i in df.columns.tolist():
    df[i] = [df[i].tolist()[x]/df_pop[i].tolist()[x] for x in [0,1,2,3]]
df.reset_index(inplace=True)

#Now lets do the congressional districts
#2010
df2010 = pd.read_excel('2010_general_results_final.xls',sheetname = 0)
df2010 = df2010[['CG','TotVoters']]
df2010.columns = ['CG','2010Votes']
df2010 = df2010.groupby(['CG']).sum()

#2012
df2012 = pd.read_excel('2012mngeneralelectionresults_official_postrecounts.xlsx',sheetname = 0)
df2012 = df2012[['CONGDIST','TOTVOTING']]
df2012.columns = ['CG','2012Votes']
df2012 = df2012.groupby(['CG']).sum()

#2014
df2014 = pd.read_excel('2014-general-federal-state-results-by-precinct-official.xlsx',sheetname = 0)
df2014 = df2014[['CONGDIST','TOTVOTING']]
df2014.columns = ['CG','2014Votes']
df2014 = df2014.groupby(['CG']).sum()

#2016
df2016 = pd.read_excel('2016-general-federal-state-results-by-precinct-official.xlsx',sheetname = 0)
df2016 = df2016[['CONGDIST','TOTVOTING']]
df2016.columns = ['CG','2016Votes']
df2016 = df2016.groupby(['CG']).sum()

#Binding all years together
df_cong = df2010.merge(df2012, left_index=True,right_index=True).merge(df2014, left_index=True,right_index=True).merge(df2016, left_index=True,right_index=True)
df_cong = df_cong.melt(value_vars = ['2010Votes','2012Votes','2014Votes','2016Votes'],
                       var_name = 'Year',
                       value_name = 'Votes')
df_cong['Year'] = [x[0:4] for x in df_cong['Year'].tolist()]
df_cong['Year'] = df_cong['Year'].astype('int')
df_cong = df_cong.merge(df,left_on = 'Year',right_on='Year')

#Lets pull in congressional populations
cong_pops = pd.read_csv('CongPopsLong.csv')
df_cong['Votes'] = [df_cong['Votes'].tolist()[x]/cong_pops['VotingPop'].tolist()[x] for x in df_cong.index.tolist()]
df_cong['District']= [1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8]
df_cong.to_csv('CongressionalTurnout.csv',index = False)