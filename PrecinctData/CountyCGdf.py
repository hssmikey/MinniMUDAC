#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 16:16:59 2018

This script is used to create our single CSV file of county votes

@author: Jacob
"""

#Loading packages
import pandas as pd
'''
#First lets get a by-county dataset
#2000
df2000 = pd.read_excel('2000_general_results.xls')
df2000 = df2000[['CC','Totl']]
df2000.columns = ['CountyCode','2000Votes']
df = df2000.groupby(['CountyCode']).sum()

#2002
df2002 = pd.read_excel('2002_general_results.xls', sheetname = 0, skiprows = 2)
df2002 = df2002[['CC','Ballots']]
df2002.columns = ['CountyCode','2002Votes']
df['2002Votes'] = df2002.groupby(['CountyCode']).sum()['2002Votes']

#2004
df2004 = pd.read_excel('2004_general_results.xls')
df2004 = df2004[['CC','TotVoters']]
df2004.columns = ['CountyCode','2004Votes']
df['2004Votes'] = df2004.groupby(['CountyCode']).sum()['2004Votes']

#2006
df2006 = pd.read_excel('2006_general_results.xls',sheetname = 0)
df2006 = df2006[['County_ID','TotVoters']]
df2006.columns = ['CountyCode','2006Votes']
df2006 = df2006.groupby(['CountyCode']).sum()['2006Votes']
df2006 = df2006[:-1]
df2006.index = [i for i in range(1,88)]
df['2006Votes'] = df2006

#2008
df2008 = pd.read_excel('2008_general_results.xls',sheetname = 0)
df2008 = df2008[['CountyID','TotVoters']]
df2008.columns = ['CountyCode','2008Votes']
df['2008Votes'] = df2008.groupby(['CountyCode']).sum()['2008Votes']
'''
#2010
df2010 = pd.read_excel('2010_general_results_final.xls',sheetname = 0)
df2010 = df2010[['CountyID',
                 'TotVoters',
                 'CONGR',
                 'CONGDFL',
                 'CONGTOT']]
df2010.columns = ['CountyCode',
                  '2010Votes',
                  '2010Votes_R',
                  '2010Votes_DFL',
                  '2010Votes_Total']
df2010 = df2010.groupby(['CountyCode']).sum()

#2012
df2012 = pd.read_excel('2012mngeneralelectionresults_official_postrecounts.xlsx',sheetname = 0)
df2012 = df2012[['COUNTYCODE',
                 'TOTVOTING',
                 'USPRSR',
                 'USPRSDFL',
                 'USPRSTOTAL']]
df2012.columns = ['CountyCode',
                  '2012Votes',
                  '2012Votes_R',
                  '2012Votes_DFL',
                  '2012Votes_Total']
df2012 = df2012.groupby(['CountyCode']).sum()

#2014
df2014 = pd.read_excel('2014-general-federal-state-results-by-precinct-official.xlsx',sheetname = 0)
df2014 = df2014[['COUNTYCODE',
                 'TOTVOTING',
                 'USSENR',
                 'USSENDFL',
                 'USSENTOTAL']]
df2014.columns = ['CountyCode',
                  '2014Votes',
                  '2014Votes_R',
                  '2014Votes_DFL',
                  '2014Votes_Total']
df2014 = df2014.groupby(['CountyCode']).sum()

#2016
df2016 = pd.read_excel('2016-general-federal-state-results-by-precinct-official.xlsx',sheetname = 0)
df2016 = df2016[['COUNTYCODE',
                 'TOTVOTING',
                 'USPRSR',
                 'USPRSDFL',
                 'USPRSTOTAL']]
df2016.columns = ['CountyCode',
                  '2016Votes',
                  '2016Votes_R',
                  '2016Votes_DFL',
                  '2016Votes_Total']
df2016 = df2016.groupby(['CountyCode']).sum()

#Binding all years together
df = df2010.merge(df2012, left_index=True,right_index=True).merge(df2014, left_index=True,right_index=True).merge(df2016, left_index=True,right_index=True)
df.columns
#Now we have to sub in county names
county_list = pd.read_excel('2016-general-federal-state-results-by-precinct-official.xlsx',sheetname = 0)
county_list = county_list[['COUNTYNAME','COUNTYCODE']].groupby(['COUNTYCODE']).first()
df = df.merge(county_list, right_index = True, left_index = True)
df = df.set_index('COUNTYNAME')

#Writing to CSV
df.to_csv('VotesByCountyByYear.csv')

#Now lets do the congressional districts
#2000
df2000 = pd.read_excel('2000_general_results.xls')
df2000 = df2000[['CG','Totl']]
df2000.columns = ['CG','2000Votes']
df = df2000.groupby(['CG']).sum()

#2002
df2002 = pd.read_excel('2002_general_results.xls', sheetname = 0, skiprows = 2)
df2002 = df2002[['CG','Ballots']]
df2002.columns = ['CG','2002Votes']
df['2002Votes'] = df2002.groupby(['CG']).sum()['2002Votes']

#2004
df2004 = pd.read_excel('2004_general_results.xls')
df2004 = df2004[['CG','TotVoters']]
df2004.columns = ['CG','2004Votes']
df['2004Votes'] = df2004.groupby(['CG']).sum()['2004Votes']

#2006
df2006 = pd.read_excel('2006_general_results.xls',sheetname = 0)
df2006 = df2006[['CG','TotVoters']]
df2006.columns = ['CG','2006Votes']
df2006 = df2006.groupby(['CG']).sum()['2006Votes']
df2006 = df2006[:-1]
df2006.index = [i for i in range(1,9)]
df['2006Votes'] = df2006

#2008
df2008 = pd.read_excel('2008_general_results.xls',sheetname = 0)
df2008 = df2008[['CG','TotVoters']]
df2008.columns = ['CG','2008Votes']
df['2008Votes'] = df2008.groupby(['CG']).sum()['2008Votes']

#2010
df2010 = pd.read_excel('2010_general_results_final.xls',sheetname = 0)
df2010 = df2010[['CG','TotVoters']]
df2010.columns = ['CG','2010Votes']
df['2010Votes'] = df2010.groupby(['CG']).sum()['2010Votes']

#2012
df2012 = pd.read_excel('2012mngeneralelectionresults_official_postrecounts.xlsx',sheetname = 0)
df2012 = df2012[['CONGDIST','TOTVOTING']]
df2012.columns = ['CG','2012Votes']
df['2012Votes'] = df2012.groupby(['CG']).sum()['2012Votes']

#2014
df2014 = pd.read_excel('2014-general-federal-state-results-by-precinct-official.xlsx',sheetname = 0)
df2014 = df2014[['CONGDIST','TOTVOTING']]
df2014.columns = ['CG','2014Votes']
df['2014Votes'] = df2014.groupby(['CG']).sum()['2014Votes']

#2016
df2016 = pd.read_excel('2016-general-federal-state-results-by-precinct-official.xlsx',sheetname = 0)
df2016 = df2016[['CONGDIST','TOTVOTING']]
df2016.columns = ['CG','2016Votes']
df['2016Votes'] = df2016.groupby(['CG']).sum()['2016Votes']

#Saving to csv
df.to_csv('VotesByCongDistByYear.csv')