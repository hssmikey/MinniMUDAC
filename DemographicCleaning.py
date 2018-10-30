#Loading libraries
import pandas as pd

#Loading datasets
vote = pd.read_csv("ACS_16_5YR_DP05_with_ann.csv", skiprows = 1)

#Subsetting the data
vote = vote[['Geography',  
             'Estimate; SEX AND AGE - Total population',
             'Estimate; RACE - One race - White',
             'Estimate; RACE - One race - Black or African American',
             'Estimate; RACE - One race - American Indian and Alaska Native',
             'Estimate; RACE - One race - Asian',
             'Estimate; RACE - One race - Native Hawaiian and Other Pacific Islander',
             'Estimate; RACE - One race - Some other race',
             'Estimate; RACE - Two or more races',
             'Estimate; HISPANIC OR LATINO AND RACE - Total population - Hispanic or Latino (of any race)'
             ]]

#Lets rename columns
vote.columns = [x.split(' - ')[-1] for x in vote.columns]

#Lets drop the MN total row
vote = vote.tail(87)

#Setting county to index
vote['Geography'] = [x.replace(' County, Minnesota','') for x in vote['Geography']]
vote.columns = ['County'] + vote.columns.tolist()[1:]
vote = vote.set_index('County')

#Now lets create all of the proportions using the population
for i in vote.columns[1:]:
    vote['Proportion '+i] = vote[i]/vote['Total population']

vote.head(5)[['Total population','White','Proportion White']]

#Save to csv for persistance
vote.to_csv('Final2016DemographicData.csv',encoding = 'utf8')