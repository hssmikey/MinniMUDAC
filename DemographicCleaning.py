# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Loading libraries
import pandas as pd

#Loading datasets
vote = pd.read_csv("ACS_16_5YR_DP05_with_ann.csv", skiprows = 1)

#Subsetting the data
vote = vote[['Geography',  
             'Estimate; RACE - Total population',
             'Estimate; RACE - Total population - One race',
             'Estimate; RACE - Total population - Two or more races',
             'Estimate; RACE - One race',
             'Estimate; RACE - One race - White',
             'Estimate; RACE - One race - Black or African American',
             'Estimate; RACE - One race - American Indian and Alaska Native',
             'Estimate; RACE - One race - American Indian and Alaska Native - Cherokee tribal grouping',
             'Estimate; RACE - One race - American Indian and Alaska Native - Chippewa tribal grouping',
             'Estimate; RACE - One race - American Indian and Alaska Native - Navajo tribal grouping',
             'Estimate; RACE - One race - American Indian and Alaska Native - Sioux tribal grouping',
             'Estimate; RACE - One race - Asian',
             'Estimate; RACE - One race - Asian - Asian Indian',
             'Estimate; RACE - One race - Asian - Chinese',
             'Estimate; RACE - One race - Asian - Filipino',
             'Estimate; RACE - One race - Asian - Japanese',
             'Estimate; RACE - One race - Asian - Korean',
             'Estimate; RACE - One race - Asian - Vietnamese',
             'Estimate; RACE - One race - Asian - Other Asian',
             'Estimate; RACE - One race - Native Hawaiian and Other Pacific Islander',
             'Estimate; RACE - One race - Native Hawaiian and Other Pacific Islander - Native Hawaiian',
             'Estimate; RACE - One race - Native Hawaiian and Other Pacific Islander - Guamanian or Chamorro',
             'Estimate; RACE - One race - Native Hawaiian and Other Pacific Islander - Samoan',
             'Estimate; RACE - One race - Native Hawaiian and Other Pacific Islander - Other Pacific Islander',
             'Estimate; RACE - One race - Some other race',
             'Estimate; RACE - Two or more races',
             'Estimate; RACE - Two or more races - White and Black or African American',
             'Estimate; RACE - Two or more races - White and American Indian and Alaska Native',
             'Estimate; RACE - Two or more races - White and Asian',
             'Estimate; RACE - Two or more races - Black or African American and American Indian and Alaska Native',
             'Estimate; RACE - Race alone or in combination with one or more other races - Total population',
             'Estimate; RACE - Race alone or in combination with one or more other races - Total population - White',
             'Estimate; RACE - Race alone or in combination with one or more other races - Total population - Black or African American',
             'Estimate; RACE - Race alone or in combination with one or more other races - Total population - American Indian and Alaska Native',
             'Estimate; RACE - Race alone or in combination with one or more other races - Total population - Asian',
             'Estimate; RACE - Race alone or in combination with one or more other races - Total population - Native Hawaiian and Other Pacific Islander',
             'Estimate; RACE - Race alone or in combination with one or more other races - Total population - Some other race',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Hispanic or Latino (of any race)',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Hispanic or Latino (of any race) - Mexican',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Hispanic or Latino (of any race) - Puerto Rican',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Hispanic or Latino (of any race) - Cuban',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Hispanic or Latino (of any race) - Other Hispanic or Latino',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Not Hispanic or Latino',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Not Hispanic or Latino - White alone',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Not Hispanic or Latino - Black or African American alone',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Not Hispanic or Latino - American Indian and Alaska Native alone',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Not Hispanic or Latino - Asian alone',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Not Hispanic or Latino - Native Hawaiian and Other Pacific Islander alone',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Not Hispanic or Latino - Some other race alone',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Not Hispanic or Latino - Two or more races',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Not Hispanic or Latino - Two or more races - Two races including Some other race',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Not Hispanic or Latino - Two or more races - Two races excluding Some other race, and Three or more races',
             'Estimate; HISPANIC OR LATINO AND RACE - Total housing units'
        ]]

#Lets rename columns
vote.columns = ['County']

vote.head()['Percent; CITIZEN, VOTING AGE POPULATION - Citizen, 18 and over population - Female']
