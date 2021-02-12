
# you must compare the other systems using evaluation metrics but actual performance of recommender system is not important

# video is about how well you can present your product. Voice over video
# explain what it is, how it works, display the best of its features, demo main functionality
# like a little sales pitch

# when reviewing papers, look at:
#   RS technique/type
#   model
#   evaluation methods used
#   limitations
# in order to get an idea of common or good or useful combinations of systems

# restaurants

import json
from surprise import SVD
from surprise import Dataset
from surprise import Reader
import texttable
import pandas as pd
from surprise import BaselineOnly
from surprise.model_selection import cross_validate
from surprise.model_selection import train_test_split
from surprise import accuracy

def getRecommendations(uid): # 
    file_path = 'processed/reviews.csv'
    reader = Reader(line_format='user item rating', sep=',')
    data = Dataset.load_from_file(file_path, reader=reader)
    #cross_validate(BaselineOnly(), data, verbose=True) # base line comparison
    #cross_validate(SVD(),data, verbose=True)
    #algo = BaselineOnly()
    #trainset = data.build_full_trainset()
    #trainset,testset = train_test_split(data, test_size=.25) # for evaluation purposes
    algo = SVD()
    print('Getting recommendations for {} of {} restaurants in {}...'.format(name,category,city))
    algo.fit(trainset)
    suggestions = {}
    for iid in iids:
        if iid in businesses and category in businesses[iid]['categories']: # knowledge based filtering
            pred = algo.predict(uid,iid) # predict what user uid will rate item iid
            suggestions[pred[1]] = pred[3] # collaborative filtering
    suggestions = sorted(suggestions.items(), key=lambda item: item[1],reverse=True)
    return suggestions[:8] # present top 8 restaurants

def presentRecommendations(items): # takes items from recommender and displays them in an appealing way
    if items == []:
        print('There are no {} restaurants in {}'.format(category,city))
        return None
    print('''
These recommendations are based on: 
    1. Your previous ratings of these restaurants (if any)
    2. The opinions of other users with similar preferences to you
    3. The city you said you were closest to ({})
    4. The category of food you selected ({})
    '''.format(city,category))
    table = texttable.Texttable(max_width=100)
    table.set_cols_dtype(['i','t','t','t','t']) # specify data types
    table.set_cols_align(['c','l','c','c','c']) # align columns horizontally
    table.set_cols_valign(['m','m','m','m','m']) # align columns vertically
    rows = [['Number','Name', 'City', 'Average Rating','Your Predicted Rating']] # titles of columns
    i = 1
    for item in items:
        iid = item[0]
        predRating = f'{item[1]:.2f}' # round to 2 d.p
        business = businesses[iid]
        rows.append([i,business['name'],business['city'],business['stars'],predRating])
        i += 1
    table.add_rows(rows)
    print(table.draw())
    print()
    print('Select a restaurant to see more information: (1-{})'.format(len(items)))
    check = False
    while not check:
        choice = input('Your Choice > ').strip()
        try:
            choice = int(choice)
            if 1 <= choice <= len(items):
                check = True
        except:
            pass
    chosen = items[choice-1]
    return chosen[0],f'{chosen[1]:.2f}'

def moreInformation(restaurant,predRating):
    if restaurant == None:
        return
    business = businesses[restaurant]
    restaurantName = business['name']
    address = '{}\n{}, {}'.format(business['address'],business['city'],business['state'])
    features = covidFeatures[restaurant]
    delivery = features['delivery or takeout']
    delivery = 'Yes' if delivery=='TRUE' else 'No'
    grubhub = features['Grubhub enabled']
    grubhub = 'Yes' if grubhub=='TRUE' else 'No'
    message = features['Covid Banner']
    closed = features['Temporary Closed Until']
    
    table = texttable.Texttable(max_width=100) # more detailed information table
    table.set_cols_dtype(['t','t','t','t','t','t','t'])
    table.set_cols_align(['l','c','c','c','c','c','c'])
    table.set_cols_valign(['m','m','m','m','m','m','m'])
    table.add_rows([['Name','Address','Number of Reviews','Average Rating','Predicted Rating','Delivery or Takeout','Grubhub'],
    [restaurantName,address,business['review_count'],business['stars'],predRating,delivery,grubhub]])
    print(table.draw())
    print()

    table = texttable.Texttable() # normal opening hours table
    table.set_deco(texttable.Texttable.HEADER)
    table.set_cols_dtype(['t','t'])
    table.set_cols_align(['l','l'])
    rows = [['Opening Hours:','']]
    hours = business['hours']
    if hours != None:
        for day in hours:
            times = hours[day].replace(':0',':00')
            rows.append([day,times])
        table.add_rows(rows)
        print(table.draw())

    if closed != 'FALSE': # extra covid data, if present for particular restaurant
        print()
        print('{} is/was closed temporarily until {}\n'.format(restaurantName,closed.split('T')[0]))
    if message != 'FALSE' and message != '':
        print()
        print('Covid message from {}:\n'.format(restaurantName))
        print(message)
        print()
    print('''
What do you want to do?
1. Give a rating of {}
2. See the list again
3. Return to main menu
    '''.format(restaurantName))
    while True:
        choice = input('Your Choice > ').strip()
        try:
            choice = int(choice)
            if choice == 1:
                print('''
How many stars do you want to give {}? (1-5)
                '''.format(restaurantName))
                while True:
                    stars = input('Your Rating > ').strip()
                    try:
                        stars = int(stars)
                        if 1 <= stars <= 5:
                            reviews = open('processed/reviews.csv','a') # add new rating to reviews file
                            reviews.write('{},{},{}\n'.format(uid,restaurant,stars))
                            reviews.close()
                            break
                    except:
                        pass
                print('\nYou gave {} a rating of {} stars\n'.format(restaurantName,stars))
                input('Press enter to return to main menu ')
                return False
            if choice == 2:
                return True
            elif choice == 3:
                return False
        except:
            pass

def info(): # explain how the system works, for transparency and explainability
    print('''
Which data do we collect from you?

    We collect 3 things from you:
        1. The city you specify
        2. The type of food you specify
        3. Any ratings you give

How is it collected?

    Explicitly, from the choices you make when prompted.

For what purpose?

    In order for us to suggest more relevant restaurants that you might like.

    ''')
    input('Press enter to return to main menu ')


def menu(): # main menu
    print('''

***** Main Menu *****

What would you like to do?

1. Change user
2. Change category
3. Change city
4. Get recommendations
5. Information
q. Quit
    ''')
    check = False
    while not check:
        choice = input('Your Choice > ').strip()
        try:
            choice = int(choice)
            if 1 <= choice <= 5:
                check = True
        except:
            if choice == 'q' or choice == 'Q':
                print('Goodbye.')
                exit()
    return choice

def welcome():
    print('Welcome to the hybrid recommender system using the Yelp dataset!\n')

def whichCity(): # 10 cities included in dataset
    cities = ['Montreal','Calgary','Toronto','Pittsburgh','Charlotte',
    'Urbana-Champaign','Phoenix','Las Vegas','Madison','Cleveland']
    question = '''
Which city are you closest to, {}?
    '''.format(name)
    for i in range(len(cities)):
        question += '''
{}. {}'''.format(i+1,cities[i])
    print(question)
    print()
    check = False
    while not check:
        choice = input('Your Choice > ').strip()
        try:
            choice = int(choice)
            if 1 <= choice <= len(cities):
                check = True
        except:
            pass
    return cities[choice-1]

def getCategory(): # 12 most popular cuisines from dataset
    categories = ['American', 'Mexican', 'Italian', 'Chinese', 'Seafood', 'Japanese', 
    'Canadian', 'Mediterranean', 'Indian', 'Thai', 'Middle Eastern', 'Vietnamese']
    question = '''
What type of food are you looking for, {}?
    '''.format(name)
    for i in range(len(categories)):
        question += '''
{}. {}'''.format(i+1,categories[i])
    print(question)
    print()
    check = False
    while not check:
        choice = input('Your Choice > ').strip()
        try:
            choice = int(choice)
            if 1 <= choice <= len(categories):
                check = True
        except:
            pass
    return categories[choice-1]

def getID(): # validate the user ID
    count = 0
    ID = ''
    while ID == '':
        ID = input('Enter your user ID > ').strip()
        try:
            name = users[ID] # check if user_id is a real user
            print('Hello, {}'.format(name))
        except:
            ID = ''
    return ID, name

if __name__ == '__main__':
    welcome()
    usersFile = open('processed/users.json','r') # load these 3 json files here to save time later
    users = json.load(usersFile)
    usersFile.close()
    businessesFile = open('processed/businesses.json','r')
    businesses = json.load(businessesFile)
    businessesFile.close()
    covidFile = open('processed/covid.json','r')
    covidFeatures = json.load(covidFile)
    covidFile.close()

    uid, name = getID()
    category = getCategory()
    city = whichCity()
    cityRestaurants = open('processed/cities/'+city+'.json','r')
    iids = json.load(cityRestaurants)
    cityRestaurants.close()
    items = getRecommendations(uid)
    moreInfo = True
    while moreInfo:
        restaurant,predRating = presentRecommendations(items)
        moreInfo = moreInformation(restaurant,predRating)
    
    while True: # after first run-through, present main menu and let user change options and investigate system
        choice = menu()
        if choice == 1:
            uid, name = getID()
        elif choice == 2:
            category = getCategory()
        elif choice == 3:
            city = whichCity()
            cityRestaurants = open('processed/cities/'+city+'.json','r')
            iids = json.load(cityRestaurants)
            cityRestaurants.close()
        elif choice == 4:
            items = getRecommendations(uid)
            moreInfo = True
            while moreInfo:
                restaurant,predRating = presentRecommendations(items)
                moreInfo = moreInformation(restaurant,predRating)
        elif choice == 5:
            info()
