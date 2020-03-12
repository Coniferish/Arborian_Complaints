import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

url = 'https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-population.csv'
uspop = pd.read_csv(url)
#print(uspop.head())

uspopyr = uspop[uspop['ages']=='total']
uspopyr = uspopyr.drop('ages',1).groupby(['year', 'state/region']).sum()
uspop2013 = uspopyr.xs(2013)
uspop2013 = pd.Series(uspop2013['population'])
# print(type(us2013))
# print(uspop2013.head())

with open('C:/Users/John J/Documents/01_Arborian/complaints.csv', 'r', encoding = 'utf8') as open_file:
    # print(open_file.read(500))
    complaints = pd.read_csv(open_file)
    # print(complaints.head())
    df_states = complaints[['State', 'Complaint ID']]
    state_complaints = df_states.groupby('State').count()
    state_complaints = state_complaints.rename(columns = {'Complaint ID': 'Number of Complaints'})
    print(state_complaints.head())
    #print(type(state_complaints))

    complaints_pop = pd.concat([uspop2013, state_complaints], axis = 1, join = 'inner')
    print(complaints_pop.head())
    
    pd.options.mode.chained_assignment = None
    df_per_yr = complaints[['Date received', 'Complaint ID']]
    df_per_yr['Date received'] = df_per_yr['Date received'].str.slice(0,4)
    df_per_yr.rename({'Complaint ID' : 'Number of Complaints', 'Date received' : 'Year'}, axis = 1, inplace = True)
    complaints_per_yr = df_per_yr.groupby('Year').count()
    print(complaints_per_yr.head())

complaints_pop = pd.concat([uspop2013, state_complaints], axis = 1, join = 'inner')
# print(complaints_pop.head())

complaints_pop['per_capita'] = complaints_pop['Number of Complaints']/complaints_pop['population']
# print(complaints_pop.head())

most_complaining_ist = complaints_pop.nlargest(10, 'per_capita')
print(most_complaining_ist['per_capita'])

complaints_pop.nlargest(5, 'per_capita').plot.bar(title = '5 Most Complaining-ist States', y = 'per_capita')
plt.show()

#print(complaints_per_yr.head())
complaints_per_yr.plot(title = 'Total Complaints per Year', y = 'Number of Complaints')
plt.show()