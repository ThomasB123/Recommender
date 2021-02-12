
import json
import pandas as pd


def getIDs():
    inFile = open('processed/2019business.json','r')
    outFile = open('processed/business_ids.json','w')
    ids = {}
    categories = ['American', 'Mexican', 'Italian', 'Chinese', 'Seafood', 'Japanese', 'Canadian', 'Mediterranean', 'Indian', 'Thai', 'Middle Eastern', 'Vietnamese']
    for line in inFile:
        business = json.loads(line)
        ID = business['business_id']
        busCategories = business['categories']
        try:
            if business['is_open'] == 1 and 'Restaurants' in busCategories:
                check = False
                for category in categories:
                    if category in busCategories:
                        check = True
                        break
                if check:
                    ids[ID] = {}
                    for attribute in ['name','address','city','state','postal_code','latitude','longitude','stars','review_count','attributes','categories','hours']:
                        ids[ID][attribute] = business[attribute]
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

def lastCheckin():
    inFile = open('processed/checkin.json','r')
    outFile = open('processed/lastCheckin.json','w')
    last = {}
    for line in inFile:
        business = json.loads(line)
        ID = business['business_id']
        checkins = business['date'].split(', ')
        last[ID] = checkins[-1]
    json.dump(last,outFile)
    inFile.close()
    outFile.close()

def recentCheckin():
    lastFile = open('processed/lastCheckin.json','r')
    last = json.load(lastFile)
    lastFile.close()
    inFile = open('processed/business.json','r')
    outFile = open('processed/2019business.json','w')
    for line in inFile:
        business = json.loads(line)
        ID = business['business_id']
        if ID in last and last[ID][:4] == '2019':
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
        if userIDs[user] > 500:
            print(user, userIDs[user])

def filterMostActiveReviews():
    users = ['CxDOIDnH8gp9KXzpBHJYXw','ELcQDlf69kb-ihJfxZyL0A','bLbSNkLggFnqwNNzzq-Ijw','U4INQZOPSUaj8hMjLlZ3KA',
    'DK57YibC5ShBmqQl97CKog','d_TBs6J3twMy9GChqUEXkg','PKEzKWv_FktMm2mGPjwd0Q','cMEtAiW60I5wE_vLfTxoJQ',
    'V-BbqKqO8anwplGRx9Q5aQ']
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
    panda = pd.read_json('processed/usefulReviews.json',lines=True)
    panda = panda.drop(['review_id','useful','funny','cool','text','date'],axis=1)
    panda.to_csv('processed/usefulReviews.csv',index=False)
    '''
    inFile = open('processed/review.json','r')
    outFile = open('processed/review.csv','w')
    for line in inFile:
        review = json.loads(line)
        #outFile.write(review['user_id']+','+review['business_id']+','+str(review['stars'])+','+review['date']+'\n')
        outFile.write('{},{},{},{}\n'.format(review['user_id'],review['business_id'],int(review['stars']),review['date']))
    inFile.close()
    outFile.close()
    '''

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

def filterUsefulReviews():
    inFile = open('processed/review.json','r')
    outFile = open('processed/usefulReviews.json','w')
    for line in inFile:
        review = json.loads(line)
        if review['useful'] > 4:
            outFile.write(line)
    inFile.close()
    outFile.close()

def filterRecentReviews():
    inFile = open('processed/review.json','r')
    outFile = open('processed/recentReviews.json','w')
    for line in inFile:
        review = json.loads(line)
        if review['date'][:4] == '2019':
            outFile.write(line)
    inFile.close()
    outFile.close()

def splitReviews():
    inFile = open('processed/usefulReviews.json','r')
    closestCity = open('processed/closestCity.json','r')
    closest = json.load(closestCity)
    closestCity.close()
    for line in inFile:
        review = json.loads(line)
        closestCity = closest[review['business_id']]
        with open('processed/cities/'+closestCity+'_usefulReviews.json','a') as fout:
            fout.write(line)
    inFile.close()

def getCategories():
    inFile = open('processed/business.json','r')
    outFile = open('processed/categories.json','w')
    allCategories = {}
    for line in inFile:
        business = json.loads(line)
        #categories = business['categories'].split(', ')
        allCategories[business['business_id']] = business['categories']
        #for category in categories:
        #    allCategories[business]
        #    if category in allCategories:
        #        allCategories[category] += 1
        #    else:
        #        allCategories[category] = 1
    #sortedDict = dict(sorted(allCategories.items(),key=lambda item: item[1]))
    #print(sortedDict)
    json.dump(allCategories,outFile)
    inFile.close()
    outFile.close()

def formatCovidFeatures():
    inFile = open('processed/covid_features.json','r')
    outFile = open('processed/covid.json','w')
    features = {}
    for line in inFile:
        business = json.loads(line)
        ID = business['business_id']
        features[ID] = {}
        for attribute in ['highlights','delivery or takeout','Grubhub enabled','Covid Banner','Temporary Closed Until']:
            features[ID][attribute] = business[attribute]
    json.dump(features,outFile)
    inFile.close()
    outFile.close()

def closedCovid():
    lastFile = open('processed/covid.json','r')
    covid = json.load(lastFile)
    lastFile.close()
    inFile = open('processed/business.json','r')
    outFile = open('processed/open2019Business.json','w')
    for line in inFile:
        business = json.loads(line)
        ID = business['business_id']
        if covid[ID]['Temporary Closed Until'] == 'FALSE':
            outFile.write(line)
    inFile.close()
    outFile.close()

def getDemoIDs():
    inFile = open('processed/usefulReviews.json','r')
    uids = {}
    for line in inFile:
        review = json.loads(line)
        uid = review['user_id']
        if uid in uids:
            uids[uid] += 1
        else:
            uids[uid] = 1
    inFile.close()
    print(sorted(uids.items(), key=lambda item: item[1]))
    print(len(uids))

def getNumberRestaurants():
    inFile = open('dataset/business.json','r')
    count = 0
    for line in inFile:
        business = json.loads(line)
        ID = business['business_id']
        busCategories = business['categories']
        if busCategories != None and 'Restaurants' in busCategories:
            count += 1
    inFile.close()
    print(count)

#ids = getIDs()
#filterRelevant()
#lastCheckin()
#recentCheckin()
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
#splitIDs()
#filterUsefulReviews()
#filterRecentReviews()
#splitReviews()
#getCategories()
#formatCovidFeatures()
#closedCovid()
#getDemoIDs()
getNumberRestaurants()
