
import json
import pandas as pd


def getIDs():
    inFile = open('dataset/business.json','r')
    outFile = open('processed/business_ids.json','w')
    ids = {}
    for line in inFile:
        business = json.loads(line)
        ID = business['business_id']
        try:
            if business['is_open'] == 1 and 'Restaurant' in business['categories']:
                ids[ID] = business['name']
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

def covidDuplicates():
    inFile = open('processed/covid_features.json')
    duplicates = ['D35unF350QG06LXDe0Cv-Q','nLGgJBtMfGv7_juXipXheA','b5uCtk5iUcdeSWBNAx40Ug','l3joBBpkq0ib11dKUpKMAw','4v0aj1VWtNwvzOeQ2Ohzrg','BpL-s3p572cxNdXJAsahpA','ZBfoUKOkfocsYK6TFQpwaA','s2Fv9gzUnnpfnkUTAMSK7w']
    for line in inFile:
        business = json.loads(line)
        ID = business['business_id']
        if ID in duplicates:
            print(line)

def getUserIDs():
    inFile = open('dataset/user.json','r')
    outFile = open('processed/user_ids.json','w')
    userIDs = {}
    for line in inFile:
        user = json.loads(line)
        userIDs[user['user_id']] = user['name']
    json.dump(userIDs,outFile)
    inFile.close()
    outFile.close()
    return userIDs

def mostActiveUsers():
    inFile = open('dataset/user.json','r')
    #outFile = open('processed/activeUsers.json','w')
    userIDs = {}
    for line in inFile:
        user = json.loads(line)
        count = user['review_count']
        if count > 10000:
            print(count)
    #json.dump(userIDs,outFile)
    inFile.close()
    #outFile.close()
    #return userIDs

def numberRestaurantReviews():
    inFile = open('processed/review.json','r')
    outFile = open('processed/numberReviews.json','w')
    userIDs = {}
    for line in inFile:
        review = json.loads(line)
        user = review['user_id']
        if user in userIDs:
            userIDs[user] += 1
        else:
            userIDs[user] = 1
    json.dump(userIDs,outFile)
    inFile.close()
    outFile.close()

def mostReviews():
    inFile = open('processed/numberReviews.json','r')
    userIDs = json.load(inFile)
    for user in userIDs:
        if userIDs[user] > 600:
            print(user, userIDs[user])

def filterMostActiveReviews():
    users = ['CxDOIDnH8gp9KXzpBHJYXw','ELcQDlf69kb-ihJfxZyL0A','bLbSNkLggFnqwNNzzq-Ijw','U4INQZOPSUaj8hMjLlZ3KA',
    'DK57YibC5ShBmqQl97CKog','d_TBs6J3twMy9GChqUEXkg','PKEzKWv_FktMm2mGPjwd0Q','cMEtAiW60I5wE_vLfTxoJQ',
    'MMf0LhEk5tGa1LvN7zcDnA','V-BbqKqO8anwplGRx9Q5aQ']
    inFile = open('processed/review.json','r')
    outFile = open('processed/mostActiveReviews.json','w')
    for line in inFile:
        review = json.loads(line)
        if review['user_id'] in users:
            outFile.write(line)
    inFile.close()
    outFile.close()

def uniqueRestaurants():
    for ID in users:
        inFile = open('processed/mostActiveReviews.json','r')
        businesses = {}
        for line in inFile:
            review = json.loads(line)
            if review['user_id'] == ID:
                business = review['business_id']
                if business in businesses:
                    businesses[business] += 1
                else:
                    businesses[business] = 1
        inFile.close()
        print(len(businesses),businesses[max(businesses,key=businesses.get)])

def dropText():
    panda = pd.read_json('processed/mostActiveReviews.json',lines=True)
    panda = panda.drop(['review_id','useful','funny','cool','text'],axis=1)
    panda.to_csv('processed/mostActiveReviews.csv',index=False)


def splitCities():
    cities = {'Montreal':(45.50884,-73.58781),'Calgary':(51.05011,-114.08529),'Toronto':(43.70011,-79.4163),
    'Pittsburgh':(40.44062,-79.99589),'Charlotte':(35.22709,-80.84313),'Urbana-Champaign':(40.11059,-88.20727),
    'Phoenix':(33.44838,-112.07404),'Las Vegas':(36.17497,-115.13722),'Madison':(43.07305,-89.40123),
    'Cleveland':(41.4995,-81.69541)}
    inFile = open('processed/business.json','r')
    outFile = open('processed/closestCity.json','w')
    closest = {}
    for line in inFile:
        business = json.loads(line)
        lat = business['latitude']
        lon = business['longitude']
        smallest = 100000
        closestCity = ''
        for city in cities:
            coords = cities[city]
            distance = (coords[0]-lat)**2+(coords[1]-lon)**2
            if distance < smallest:
                smallest = distance
                closestCity = city
        closest[business['business_id']] = closestCity
        with open('processed/cities/'+closestCity+'.json','a') as fout:
            fout.write(line)
    json.dump(closest,outFile)
    inFile.close()
    outFile.close()

def splitIDs():
    cities = ['Montreal','Calgary','Toronto','Pittsburgh','Charlotte',
    'Urbana-Champaign','Phoenix','Las Vegas','Madison','Cleveland']
    for city in cities:
        ids = {}
        inFile = open('processed/cities/'+city+'.json','r')
        outFile = open('processed/cities/'+city+'_ids.json','w')
        for line in inFile:
            business = json.loads(line)
            ids[business['business_id']] = business['name']
        json.dump(ids,outFile)
        inFile.close()
        outFile.close()
    

#ids = getIDs()
#filterRelevant()
#toCSV()
#covidDuplicates()
#userIDs = getUserIDs()
#mostActiveUsers()
#numberRestaurantReviews()
#mostReviews()
#filterMostActiveReviews()
#uniqueRestaurants()
#dropText()
#splitCities()
splitIDs()

# user features: user_id, name, review_count, yelping_since, useful, funny, cool, elite, friends, fans, average_stars, compliment_hot, compliment_more, compliment_profile, compliment_cute, compliment_list, compliment_note, compliment_plain, compliment_cool, compliment_funny, compliment_writer, compliment_photos

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