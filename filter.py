
import os
import json
import pandas as pd


def getIDs():
    inFile = open('dataset/business.json','r')
    outFile = open('processed/business_ids.json','w')
    ids = {}
    count = 0
    for line in inFile:
        business = json.loads(line)
        ID = business['business_id']
        try:
            if business['is_open'] == 1 and 'Restaurant' in business['categories']:
                ids[ID] = 1
        except:
            pass
    json.dump(ids,outFile)
    inFile.close()
    outFile.close()
    return ids

def filterRelevant():
    files = ['business.json','checkin.json','review.json','tip.json','covid_features.json']
    for fileName in files:
        inFile = open('dataset/'+fileName,'r')
        outFile = open('processed/'+fileName,'w')
        for line in inFile:
            business = json.loads(line)
            if business['business_id'] in ids:
                outFile.write(line)
        inFile.close()
        outFile.close()

def toCSV():
    files = ['business','checkin','review','tip','covid_features']
    for fileName in files:
        panda = pd.read_json('processed/'+fileName+'.json', lines=True)
        panda.to_csv('processed/'+fileName+'.csv',index=False)

#ids = getIDs()
#filterRelevant()
#toCSV()

inFile = open('processed/covid_features.json')
duplicates = ['D35unF350QG06LXDe0Cv-Q',
'nLGgJBtMfGv7_juXipXheA',
'b5uCtk5iUcdeSWBNAx40Ug',
'l3joBBpkq0ib11dKUpKMAw',
'4v0aj1VWtNwvzOeQ2Ohzrg',
'BpL-s3p572cxNdXJAsahpA',
'ZBfoUKOkfocsYK6TFQpwaA',
's2Fv9gzUnnpfnkUTAMSK7w']
for line in inFile:
    business = json.loads(line)
    ID = business['business_id']
    if ID in duplicates:
        print(line)


# user features: user_id, name, review_count, yelping_since, useful, funny, cool, elite, friends, fans, average_stars, compliment_hot, compliment_more, compliment_profile, compliment_cute, compliment_list, compliment_note, compliment_plain, compliment_cool, compliment_funny, compliment_writer, compliment_photos

'''


df_b = pd.read_json(business_json_path, lines=True)

df_b = df_b[df_b['is_open'] == 1]

drop_columns = ['is_open']
df_b = df_b.drop(drop_columns, axis=1)

business_restaurant = df_b[df_b['categories'].str.contains('Restaurants',case=False,na=False)]

#df_explode = df_b.assign(categories = df_b.categories.str.split(', ')).explode('categories')

#print(df_explode.categories.value_counts())

#print(df_explode[df_explode['categories'].str.contains('Restaurants',case=True,na=False)].categories.value_counts())

csv_name = 'processedData/business_restaurants.csv'
business_restaurant.to_csv(csv_name, index=False)

# make dictionary of business IDs for restaurants only and filter tips,reviews, checkins for only those businesses

# filter by time
# get number of reviews in last year?
'''

'''
# filter dataset by city

states = {}
with open('yelp_dataset/yelp_academic_dataset_business.json') as f:
    for line in f:
        business = json.loads(line)
        state = business['state']
        city = business['city']
        if state not in states:
            states[state] = {city:1}
        else:
            if city not in states[state]:
                states[state][city] = 1
            else:
                states[state][city] = states[state][city] + 1
print(states)

for state in states:
    with open('processedData/'+state+'.txt','w') as fout:
        for city in states[state]:
            if states[state][city] > 1:
                fout.write(city + '\n')



print(data)
states = []

for business in data:
    state = business['state']
    if state not in states:
        states.append(states)

print(states)

'''