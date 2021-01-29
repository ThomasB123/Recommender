
import json
import pandas as pd


business_json_path = 'yelp_dataset/yelp_academic_dataset_business.json'
'''
totalCount = 0
openCount = 0
with open('yelp_dataset/yelp_academic_dataset_business.json','r') as f:
    with open('processedData/business_filtered.json','w') as fout:
        for line in f:
            business = json.loads(line)
            isOpen = business['is_open']
            if isOpen == 1:
                openCount += 1
                fout.write(line)
            totalCount += 1
print(openCount)
print(totalCount)
'''

df_b = pd.read_json(business_json_path, lines=True)

df_b = df_b[df_b['is_open'] == 1]

drop_columns = ['is_open']
df_b = df_b.drop(drop_columns, axis=1)

business_restaurant = df_b[df_b['categories'].str.contains('Restaurants',case=False,na=False)]

df_explode = df_b.assign(categories = df_b.categories.str.split(', ')).explode('categories')

print(df_explode.categories.value_counts())

print(df_explode[df_explode['categories'].str.contains('Restaurants',case=True,na=False)].categories.value_counts())

csv_name = 'processedData/business_restaurants.csv'
business_restaurant.to_csv(csv_name, index=False)


# filter by time
# get number of reviews in last year?



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