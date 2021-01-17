
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


if __name__ == '__main__':
    print('Welcome to the hybrid recommender system using the Yelp dataset!')
    while True:
        choice = menu()
        if choice == 1:
            pass
        elif choice == 2:
            pass
        elif choice == 3:
            info()