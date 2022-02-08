import os

SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                       'tourdeflask.sqlite')

SQLALCHEMY_TRACK_MODIFICATIONS = False
PLATFORM = 'heroku'
