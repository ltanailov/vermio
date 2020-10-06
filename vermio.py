#!/usr/bin/env python

__author__ = "Luka Tanailov"
__copyright__ = "Copyright 2016, Vermio"
__license__ = "Freemium"
__version__ = "1.2"
__maintainer__ = "Luka Tanailov"
__email__ = "luka.tanailov@gmail.com"
__status__ = "Development"


import tweepy
import webbrowser
import os


# Авторизация через Twitter ПИН-код
def authorize():
    consumer_key = 'V3tp8FuZG63VZWC0BkgPxmvvv'
    consumer_secret = 'GF78g3Rn9hr0I2mUo3OBIC82Wa4D39k59aHtWjZRKbg3G1oEsf'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()
    webbrowser.open(auth_url)
    verifier = input("Enter PIN: ")
    auth.get_access_token(verifier)
    twitterapi = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=4)
    os.system('cls')
    print("%s is logged in!" % twitterapi.me().screen_name)
    return twitterapi


# Подписывается на подисчиков, на которых пользователь еще не подписался
def award(api):
    for follower in tweepy.Cursor(api.followers).items():
        source, target = api.show_friendship(target_screen_name=follower.screen_name)
        if source.following == False:
            try:
                follower.follow()
                print("- followed %s" % follower.screen_name)
            except tweepy.TweepError as e:
                if e.api_code == 160:
                    print("- request already sent to %s" % follower.screen_name)
                else:
                    print(e)
        else:
            print("- %s is already your follower" % follower.screen_name)
    os.system('cls')


# Подписывается на подписчиков какого-либо пользователя
def hunt(api):
    mission = input("Enter Twitter nickname of target: ")
    for follower in tweepy.Cursor(api.followers, screen_name=mission).items():
        source, target = api.show_friendship(source_screen_name=api.me().screen_name,
                                             target_screen_name=follower.screen_name)
        if source.following == False:
            try:
                follower.follow()
                print("- followed %s" % follower.screen_name)
            except tweepy.TweepError as e:
                if e.api_code == 160:
                    print("- request already sent to %s" % follower.screen_name)
                else:
                    print(e)
        else:
            print("- %s is already your follower" % follower.screen_name)
    os.system('cls')


# Отписывается от не-подписчиков
def punish(api):
    for friend in tweepy.Cursor(api.friends).items():
        source, target = api.show_friendship(source_screen_name=api.me().screen_name,
                                             target_screen_name=friend.screen_name)
        if target.following == False:
            try:
                friend.unfollow()
                print("- unfollowed %s" % friend.screen_name)
            except tweepy.TweepError as e:
                print(e)
        else:
            print("- %s is your follower" % friend.screen_name)
    os.system('cls')


# Отписывается от всех
def genocide(api):
    for friend in tweepy.Cursor(api.friends).items():
        try:
            friend.unfollow()
            print("- unfollowed %s" % friend.screen_name)
        except tweepy.TweepError as e:
            print(e)
    os.system('cls')


# Главное меню и выбор действия
def init():
    api = authorize()
    os.system('cls')
    menu = {}
    menu['1'] = "Follow your followers"
    menu['2'] = "Follow target's followers"
    menu['3'] = "Unfollow non-followers"
    menu['4'] = "Unfollow all"
    menu['5'] = "Exit"
    while True:
        print("Welcome to the Vermio Twitter-bot!")
        for key in sorted(menu.keys()):
            print(key, menu[key])
        selection = input("Enter choice [1-5]: ")
        os.system('cls')
        if selection == '1':
            award(api)
        elif selection == '2':
            hunt(api)
        elif selection == '3':
            punish(api)
        elif selection == '4':
            genocide(api)
        elif selection == '5':
            break
        else:
            input("Error! Press Enter and try again!")


# Запуск программы
init()
