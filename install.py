#!/usr/bin/env
import os

try:
    import tweepy
except ImportError:
    print("Installing Tweepy")
    os.system('pip install tweepy')

input("Install complete! Press Enter!")