import os
import json

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' }]

basedir = os.path.abspath(os.path.dirname(__file__))



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

CINEMA_TO_SHOW = 3

CURRENT_USER_FACTORS_PATH = os.path.join(basedir,'recommenders/als_user_factors.npy')
CURRENT_ITEM_FACTORS_PATH = os.path.join(basedir,'recommenders/als_item_factors.npy')

CURRENT_FLASH_PATH = os.path.join(basedir,'app/static/flash_russian.json')

with open(CURRENT_FLASH_PATH) as json_file:
    flash_messages = json.load(json_file)
