
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

import os
import json
from collections import defaultdict
#from surprise import BaselineOnly
from surprise import SVD
from surprise import Dataset
from surprise import Reader
#from surprise.model_selection import cross_validate
import texttable
import pandas as pd
import numpy as np
import math
import pickle
import time

def collaborativeFiltering():
    ratings = pd.read_csv('processed/usefulReviews.csv', encoding='"ISO-8859-1"')
    ratings = ratings.sample(frac=0.2)
    ratings_training = ratings.sample(frac=0.7)
    ratings_test = ratings.drop(ratings_training.index)
    rating_mean = ratings_training.groupby(['business_id'], as_index=False, sort=False).mean().rename(columns={'rating':'rating_mean'})[['business_id','rating_mean']]
    adjusted_ratings = pd.merge(ratings_training,rating_mean,on='business_id',how='left',sort=False)
    adjusted_ratings['rating_adjusted']=adjusted_ratings['rating']-adjusted_ratings['rating_mean']
    adjusted_ratings.loc[adjusted_ratings['rating_adjusted']==0,'rating_adjusted'] = 1e-8
    start = time.time()
    w_matrix = build_w_matrix(adjusted_ratings,False)
    end = time.time()
    print(end-start)
    print('built w_matrix')
    #predict(uid,iid,w_matrix,adjusted_ratings,rating_mean)
    recommended_restaurants = recommend(uid,w_matrix,adjusted_ratings,rating_mean)
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

def recommend(uid,w_matrix,adjusted_ratings,rating_mean,amount=8):
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
    recommendations = user_ratings_all_business.sort_values(by=['rating'],ascending=False).head(amount)
    print(recommendations['business_id'].iloc[0])
    return recommendations

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

def getRecommendations(uid):
    file_path = os.path.expanduser('processed/mostActiveReviews.csv')
    reader = Reader(line_format='user item rating timestamp', sep=',')
    data = Dataset.load_from_file(file_path, reader=reader)
    #cross_validate(BaselineOnly(), data, verbose=True)

    trainset = data.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)

    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)

    top_n = get_top_n(predictions, n=8) # get top 8 recommendations
    #print(top_n.items())
    return top_n.items()

def presentRecommendations(uid,items): # takes items from recommender and 
    businessesFile = open('processed/business_ids.json','r')
    businesses = json.load(businessesFile)
    businessesFile.close()
    usersFile = open('processed/user_ids.json','r')
    users = json.load(usersFile)
    usersFile.close()
    table = texttable.Texttable()
    table.set_cols_dtype(['i','t','t','t']) # specify data types
    table.set_cols_align(['c','l','c','c']) # align columns horizontally
    table.set_cols_valign(['m','m','m','m']) # align columns vertically
    rows = [['Number','Name', 'City', 'Stars']] # titles of columns
    for userid, user_ratings in items:
        if userid == uid:
            #print(users[uid])
            i = 1
            for (iid, _) in user_ratings:
                business = businesses[iid]
                rows.append([i,business['name'],business['city'],business['stars']])
                i += 1
                #print(businesses[iid])
            #print(users[uid], [businesses[iid] for (iid, _) in user_ratings])
    table.add_rows(rows)
    print(table.draw() + "\n")


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

1. Get recommendations
2. Give preferences
3. Information
q. Quit
    ''')
    check = False
    while not check:
        choice = input('Your choice > ')
        try:
            choice = int(choice)
            if 1 <= choice <= 3:
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
        choice = input('Your choice > ')
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
        choice = input('Your choice > ')
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
    users = json.load(open('processed/user_ids.json','r'))
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
    uid, name = getID()
    category = getCategory()
    city = whichCity()
    collaborativeFiltering()
    #items = getRecommendations(uid)
    #presentRecommendations(uid,items)
    '''
    while True:
        choice = menu()
        if choice == 1:
            pass
        elif choice == 2:
            pass
        elif choice == 3:
            info()
    '''

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