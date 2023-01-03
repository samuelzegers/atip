import csv
import sys
import requests
import numpy as np
from bs4 import BeautifulSoup
from urllib3 import disable_warnings, exceptions
from time import sleep, time
import pandas as pd

def get_code(url):
    for i in range(10):
        try:
            r = requests.get(url, verify=False, timeout=10)
            break
        except(
            requests.ConnectionError,
            requests.ConnectTimeout,
            requests.ReadTimeout,
            requests.exceptions.ChunkedEncodingError
        ):
            print("Connection error, retrying in 1s...")
            sleep(1)
    else:
        print("No connection available. Try again later.")
        sys.exit()
    code = BeautifulSoup(r.text, features="lxml")
    return code

def find_friends(user):
    following = np.array([])
    url = 'https://letterboxd.com/' + user + '/following/'
    while True:
        html = get_code(url)
        for usr in html.find_all('td', class_='table-person'):
            usr_url = usr.h3.a['href'].replace("/", "")
            following = np.append(following, usr_url)
        try:
            next_page = html.find('div', class_='pagination').find('a', class_='next')['href']
            url = 'https://letterboxd.com/' + next_page
        except(TypeError, AttributeError):
            return following

def find_reviewers(film):
    reviews = np.array([])
    url = 'https://letterboxd.com/film/' + film + '/reviews/by/activity/'
    while True:
        html = get_code(url)
        for usr in html.find_all('li', class_='film-detail'):
            usr_url = usr.a['href'].replace("/", "")
            print(usr_url)
            reviews = np.append(reviews, usr_url)
        try:
            next_page = html.find('div', class_='pagination').find('a', class_='next')['href']
            url = 'https://letterboxd.com/' + next_page
        except(TypeError, AttributeError):
            return reviews

def test_find_reviewers(film, n):
    reviews = np.empty((0,2), dtype=str)
    url = 'https://letterboxd.com/film/' + film + '/reviews/by/activity/'
    for i in range(n):
        html = get_code(url)
        for usr in html.find_all('li', class_='film-detail'):
            if usr.div.div.p.span['class'][0] == 'content-metadata':
                pass
            else:
                usr_url = usr.a['href'].replace("/", "")
                score = usr.div.div.p.span['class'][2].replace("rated-", "")
                reviews = np.append(reviews, np.array([[usr_url, score]]), axis=0)
        next_page = html.find('div', class_='pagination').find('a', class_='next')['href']
        url = 'https://letterboxd.com/' + next_page
    return reviews

def find_scores(film):
    reviews = np.empty((0,2), dtype=str)
    url = 'https://letterboxd.com/film/' + film + '/reviews/by/activity/'
    while True:
        html = get_code(url)
        for usr in html.find_all('li', class_='film-detail'):
            if usr.div.div.p.span['class'][0] == 'content-metadata':
                pass
            else:
                usr_url = usr.a['href'].replace("/", "")
                score = usr.div.div.p.span['class'][2].replace("rated-", "")
                reviews = np.append(reviews, np.array([[usr_url, score]]), axis=0)
        try:
            next_page = html.find('div', class_='pagination').find('a', class_='next')['href']
            url = 'https://letterboxd.com/' + next_page
        except(TypeError, AttributeError):
            return reviews

start = time()
usrs = test_find_reviewers('shes-funny-that-way', 150)
df = pd.DataFrame(usrs)
df.to_csv('test.csv')
end = time()
print('elapsed time is', end-start, 'seconds')
#usr.div.div.p.span['class']