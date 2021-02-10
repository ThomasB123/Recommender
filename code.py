
# first step, look at dataset, decide what services to include, start preprocessing data
# then build architecture/scheme

# personalised recomendations, not just demographic or generic
# look at the individual user and their preferences and needs, context, interests
# justify choice of models and justify all choices
# you must compare the other systems using evaluation metrics but actual performance of recommender system is not important

# command line interface
# allow user to specify their name (or other identifying property), so model allows distinct users and gives personalised recomendations

# marked on explainability

# video is about how well you can present your product. Voice over video
# explain what it is, how it works, display the best of its features, demo main functionality
# like a little sales pitch

# when reviewing papers, look at:
#   RS technique/type
#   model
#   evaluation methods used
#   limitations
# in order to get an idea of common or good or useful combinations of systems

# restaurants on yelp



#import os
import json
#from collections import defaultdict
#from surprise import BaselineOnly
from surprise import SVD
from surprise import Dataset
from surprise import Reader
#from surprise.model_selection import cross_validate
import texttable
import pandas as pd
#import numpy as np
#import math
#import pickle
#import time
'''
def collaborativeFiltering(): # code adapted from https://github.com/wwwbbb8510/baseline-rs
    ratings = pd.read_csv('processed/usefulReviews.csv', encoding='"ISO-8859-1"')
    ratings = ratings.sample(frac=0.01)
    ratings_training = ratings.sample(frac=0.7)
    ratings_test = ratings.drop(ratings_training.index)
    rating_mean = ratings_training.groupby(['business_id'], as_index=False, sort=False).mean().rename(columns={'rating':'rating_mean'})[['business_id','rating_mean']]
    adjusted_ratings = pd.merge(ratings_training,rating_mean,on='business_id',how='left',sort=False)
    adjusted_ratings['rating_adjusted']=adjusted_ratings['rating']-adjusted_ratings['rating_mean']
    adjusted_ratings.loc[adjusted_ratings['rating_adjusted']==0,'rating_adjusted'] = 1e-8
    start = time.time()
    w_matrix = build_w_matrix(adjusted_ratings,True)
    end = time.time()
    print(end-start)
    print('built w_matrix')
    #predict(uid,iid,w_matrix,adjusted_ratings,rating_mean)
    recommended_restaurants = recommend(uid,w_matrix,adjusted_ratings,rating_mean)
    presentRecommendations(recommended_restaurants)
    #items = []
    #for i in range(8):
    #    items.append(recommended_restaurants['business_id'].iloc[i])
    #print(items)
    #presentRecommendations(items)
    
    print(recommended_restaurants)
    end = time.time()
    print(end-start)

def build_w_matrix(adjusted_ratings, load_existing_w_matrix):
    w_matrix_columns = ['business_1', 'business_2', 'weight']
    w_matrix = pd.DataFrame(columns=w_matrix_columns)
    if load_existing_w_matrix:
        with open('processed/w_matrix.pkl','rb') as input:
            w_matrix = pickle.load(input)
        input.close()
    else:
        distinct_business = np.unique(adjusted_ratings['business_id'])
        i=0
        for business_1 in distinct_business:
            user_data = adjusted_ratings[adjusted_ratings['business_id'] == business_1]
            distinct_users = np.unique(user_data['user_id'])

            record_row_columns = ['user_id','business_1','business_2','rating_adjusted_1','rating_adjusted_2']
            record_business_1_2 = pd.DataFrame(columns=record_row_columns)

            for c_user_id in distinct_users:
                c_business_1_rating = user_data[user_data['user_id'] == c_user_id]['rating_adjusted'].iloc[0]
                c_user_data = adjusted_ratings[(adjusted_ratings['user_id'] == c_user_id) & (adjusted_ratings['business_id'] != business_1)]
                c_distinct_business = np.unique(c_user_data['business_id'])
                for business_2 in c_distinct_business:
                    c_business_2_rating = c_user_data[c_user_data['business_id'] == business_2]['rating_adjusted'].iloc[0]
                    record_row = pd.Series([c_user_id, business_1, business_2, c_business_1_rating, c_business_2_rating], index=record_row_columns)
                    record_business_1_2 = record_business_1_2.append(record_row, ignore_index=True)
            
            distinct_business_2 = np.unique(record_business_1_2['business_2'])
            for business_2 in distinct_business_2:
                paired_business_1_2 = record_business_1_2[record_business_1_2['business_2'] == business_2]
                sim_value_numerator = (paired_business_1_2['rating_adjusted_1']*paired_business_1_2['rating_adjusted_2']).sum()
                sim_value_denominator = np.sqrt(np.square(paired_business_1_2['rating_adjusted_1']).sum()) * np.sqrt(np.square(paired_business_1_2['rating_adjusted_2']).sum())
                sim_value_denominator = sim_value_denominator if sim_value_denominator != 0 else 1e-8
                sim_value = sim_value_numerator / sim_value_denominator
                w_matrix = w_matrix.append(pd.Series([business_1, business_2, sim_value], index=w_matrix_columns), ignore_index=True)
        
        with open('processed/w_matrix.pkl', 'wb') as output:
            pickle.dump(w_matrix, output, pickle.HIGHEST_PROTOCOL)
        output.close()
    return w_matrix

def predict(uid, business_id, w_matrix, adjusted_ratings, rating_mean):
    if rating_mean[rating_mean['business_id']==business_id].shape[0] > 0:
        mean_rating = rating_mean[rating_mean['business_id']==business_id]['rating_mean'].iloc[0]
    else:
        mean_rating = 2.5
    user_other_ratings = adjusted_ratings[adjusted_ratings['user_id']==uid]
    user_distinct_business = np.unique(user_other_ratings['business_id'])
    sum_weighted_other_ratings = 0
    sum_weights = 0
    for business_j in user_distinct_business:
        if rating_mean[rating_mean['business_id']==business_j].shape[0] > 0:
            rating_mean_j = rating_mean[rating_mean['business_id']==business_j]['rating_mean'].iloc[0]
        else:
            rating_mean_j = 2.5
        w_business_1_2 = w_matrix[(w_matrix['business_1']==business_id) & (w_matrix['business_2']==business_j)]
        if w_business_1_2.shape[0] > 0:
            user_rating_j = user_other_ratings[user_other_ratings['business_id']==business_j]
            sum_weighted_other_ratings += (user_rating_j['rating'].iloc[0]-rating_mean_j) * w_business_1_2['weight'].iloc[0]
            sum_weights += np.abs(w_business_1_2['weight'].iloc[0])
    if sum_weights == 0:
        predicted_rating = mean_rating
    else:
        predicted_rating = mean_rating + sum_weighted_other_ratings/sum_weights
    return predicted_rating

def recommend(uid,w_matrix,adjusted_ratings,rating_mean,amount=5):
    distinct_business = np.unique(adjusted_ratings['business_id'])
    user_ratings_all_business = pd.DataFrame(columns=['business_id','rating'])
    user_rating = adjusted_ratings[adjusted_ratings['user_id']==uid]
    i = 0
    for business in distinct_business:
        user_rating = user_rating[user_rating['business_id']==business]
        if user_rating.shape[0] > 0:
            rating_value = user_ratings_all_business.loc[i,'rating'] = user_rating.loc[0,business]
        else:
            rating_value = user_ratings_all_business.loc[i,'rating'] = predict(uid,business,w_matrix,adjusted_ratings,rating_mean)
        user_ratings_all_business.loc[i] = [business,rating_value]
        i += 1
    recommendations = user_ratings_all_business.sort_values(by=['rating'],ascending=False) # use this for hybrid
    closestCity = open('processed/closestCity.json','r')
    location = json.load(closestCity)
    closestCity.close()
    categoriesFile = open('processed/categories.json','r')
    categories = json.load(categoriesFile)
    categoriesFile.close()
    howMany = 0
    i = 0
    relevantRestaurants = []
    print(city)
    while howMany < amount: # get the top x many which fit location and category
        business = recommendations['business_id'].iloc[i]
        print(location[business]==city)
        print(categories[business])
        if location[business] == city and (category in categories[business]):
            relevantRestaurants.append(business)
            howMany += 1
        i += 1
    #.head(amount)
    return relevantRestaurants

def get_top_n(predictions, n=10):
    inFile = open('processed/closestCity.json','r')
    closestCity = json.load(inFile)
    inFile.close()
    top_n = defaultdict(list)
    for uidLocal, iid, true_r, est, _ in predictions:
        if uidLocal == uid and closestCity[iid] == city: # only get recommendations for active user and in city they specified
            top_n[uidLocal].append((iid, est))
    for uidLocal, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uidLocal] = user_ratings[:n]
    return top_n
'''
def getRecommendations(uid):
    file_path = 'processed/usefulReviews.csv'
    reader = Reader(line_format='user item rating timestamp', sep=',')
    data = Dataset.load_from_file(file_path, reader=reader)
    #cross_validate(BaselineOnly(), data, verbose=True)

    trainset = data.build_full_trainset()
    algo = SVD()
    #start = time.time()
    print('Getting recommendations for {} of {} restaurants in {}...'.format(name,category,city))
    algo.fit(trainset)
    #end = time.time()
    #print(end-start)
    suggestions = {}
    for iid in iids:
        if iid in categories and category in categories[iid]: # include all reviews?
            pred = algo.predict(uid,iid)#,verbose=True)#,r_ui=4, verbose=True)
            suggestions[pred[1]] = pred[3]
    suggestions = sorted(suggestions.items(), key=lambda item: item[1],reverse=True)
    #print(suggestions)
    return suggestions[:8] # present top 8 restaurants
    #testset = trainset.build_anti_testset()
    #predictions = algo.test(testset)

    #top_n = get_top_n(predictions, n=8) # get top 8 recommendations
    #print(top_n.items())
    #return top_n.items()

def hybrid():
    pass
    # use namsor to get info about person from name, then use to recommend 
    # take scores produced by SVD calculations, e.g. when there's nothing to go on
    # break ties by looking at review count, accepts credit cards, price range, attire, alcohol, 
    # reservations, takeout, good for groups, ambience, good for kids, drive thru, wifi, parking, 
    # caters, delivery, noise level, outdoor seating, has tv, good for meal, categories, hours
    # all from business.json or business_ids.json
    # TODO
    # implement hybrid properly, look at lectures to figure out how to do it 
    # nearest neighbour for e.g. best night or ambience that person likes the most
    # certain features that person seems to prefer?
    # is SVD time-aware?
    # comment code
    # write paper

def presentRecommendations(items): # takes items from recommender and 
    if items == []:
        print('There are no {} restaurants in {}'.format(category,city))
        return None
    table = texttable.Texttable()
    table.set_cols_dtype(['i','t','t','t','t']) # specify data types
    table.set_cols_align(['c','l','c','c','c']) # align columns horizontally
    table.set_cols_valign(['m','m','m','m','m']) # align columns vertically
    rows = [['Number','Name', 'City', 'Avg. Rating','Your Pred. Rating']] # titles of columns
    i = 1
    for item in items:
        iid = item[0]
        predRating = f'{item[1]:.2f}' # round to 2 d.p
        business = businesses[iid]
        rows.append([i,business['name'],business['city'],business['stars'],predRating])
        i += 1
    table.add_rows(rows)
    print()
    print(table.draw())
    print('''
These recommendations are based on: 
    1. The opinions of other users with similar preferences to you
    2. The city you said you were closest to ({})
    3. The category of food you selected ({})
    '''.format(city,category))
    print('Select a restaurant to see more information')
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
    table = texttable.Texttable()
    table.set_cols_dtype(['t','t','t','t','t','t','t'])
    table.set_cols_align(['l','c','c','c','c','c','c'])
    table.set_cols_valign(['m','m','m','m','m','m','m'])
    table.add_rows([['Name','Address','No. Reviews','Avg. Rating','Your Pred. Rating','Delivery or Takeout','Grubhub'],
    [restaurantName,address,business['review_count'],business['stars'],predRating,delivery,grubhub]])
    print(table.draw())
    print()
    # add covid information here as well
    table = texttable.Texttable()
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
    if closed != 'FALSE':
        print()
        print('{} is closed temporarily until {}\n'.format(name,closed.split('T')[0]))
    if message != 'FALSE':
        print()
        print('Covid message from {}:'.format(name))
        print(message)
        print()
    print('''
What do you want to do?
1. See the list again
2. Return to main menu
    ''')
    while True:
        choice = input('Your Choice > ').strip()
        try:
            choice = int(choice)
            if choice == 1:
                return True
            elif choice == 2:
                return False
        except:
            pass

def getPreferences():
    pass


def info():
    print('''
Which data do we collect from you?

    We collect your choices.

How is it collected?

    From the choices you input here.

For what purpose?

    In order for us to suggest things you might like.

    ''')
    input('Press enter to return ')


def menu():
    print('''
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
    print('Welcome to the hybrid recommender system using the Yelp dataset!')
    print()

def whichCity():
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

def getCategory():
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

def getID():
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
    usersFile = open('processed/user_ids.json','r') # load these 3 json files here to save time later
    users = json.load(usersFile)
    usersFile.close()
    businessesFile = open('processed/business_ids.json','r')
    businesses = json.load(businessesFile)
    businessesFile.close()
    covidFile = open('processed/covid.json','r')
    covidFeatures = json.load(covidFile)
    covidFile.close()

    uid, name = getID()
    category = getCategory()
    categoriesFile = open('processed/categories.json','r')
    categories = json.load(categoriesFile)
    categoriesFile.close()
    city = whichCity()
    cityRestaurants = open('processed/cities/'+city+'_ids.json','r')
    iids = json.load(cityRestaurants)
    cityRestaurants.close()
    #collaborativeFiltering()
    items = getRecommendations(uid)
    moreInfo = True
    while moreInfo:
        restaurant,predRating = presentRecommendations(items)
        moreInfo = moreInformation(restaurant,predRating)
    
    while True:
        choice = menu()
        if choice == 1:
            uid, name = getID()
        elif choice == 2:
            category = getCategory()
            categoriesFile = open('processed/categories.json','r')
            categories = json.load(categoriesFile)
            categoriesFile.close()
        elif choice == 3:
            city = whichCity()
            cityRestaurants = open('processed/cities/'+city+'_ids.json','r')
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

# Resources:
'''
https://www.yelp.com/dataset
https://www.yelp.com/dataset/documentation/faq
https://www.yelp-support.com/Recommended_Reviews
https://github.com/Yelp/dataset-examples/blob/master/json_to_csv_converter.py
https://towardsdatascience.com/converting-yelp-dataset-to-csv-using-pandas-2a4c8f03bd88
https://www.kaggle.com/yelp-dataset/yelp-dataset?select=yelp_academic_dataset_business.json
https://github.com/Yelp/dataset-examples/issues/43
https://surpriselib.com/
'''