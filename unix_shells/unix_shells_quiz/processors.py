import datetime

# imports results from views in an attempt to create score calculator

#from views import results

# This context processor function takes the request
# object and returns a dictionary of context variables
# to be made available to all templates.


def custom_processor(request):
    now = datetime.datetime.now()
    #welcome_message = "Welcome My Friends! ------"
    return {'DATE_TIME':now}


