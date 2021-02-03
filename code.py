
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

# bars on yelp

import json

def collaborativeFiltering():
    pass


def getRecommendations():
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
    cities = ['Montreal','Calgary','Toronto','Pittsburgh','Charlotte','Urbana-Champaign','Phoenix','Las Vegas','Madison','Cleveland']
    question = '''
Which city are you closest to?
    '''
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

def getName():
    count = 0
    name = ''
    while name == '':
        name = input('What is your name? > ').strip()
    users = open('dataset/user.json','r')
    for line in users:
        user = json.loads(line)
        if user['name'] == name:
            #print(user['user_id'])
            count += 1
    print(count)


if __name__ == '__main__':
    welcome()
    getName()
    city = whichCity()
    print(city)
    
    while True:
        choice = menu()
        if choice == 1:
            pass
        elif choice == 2:
            pass
        elif choice == 3:
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