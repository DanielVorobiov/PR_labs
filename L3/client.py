import requests
import re
from threading import *

sem = Semaphore(1)


def showNews(news, t_id):
    authors = re.findall('(?<=author":)(.*?)(?=,"title)', str(news.text))
    titles = re.findall('(?<=title":)(.*?)(?=,"description)', str(news.text))
    urls = re.findall('(?<=url":)(.*?)(?=,"urlToImage)', str(news.text))

    for author, title, url in zip(authors[t_id - 1::2], titles[t_id - 1::2],
                                  urls[t_id - 1::2]):
        sem.acquire()
        if author != "null":
            print("Author: " + author)
        else:
            pass
        print("Title: " + title)
        print("URL: " + url)
        print("----------------")
        sem.release()


def categoryPick():
    print("Pick a Category: ")
    categories = [
        "Business", "Entertainment", "General", "Health", "Science", "Sports",
        "Technology"
    ]
    categoriesDictionary = {}
    for id, category in zip((range(1, len(categories) + 1)), categories):
        categoriesDictionary[str(id)] = category
        print(str(id) + ". " + category)
    categoryId = input("Choose an option: ")
    print(categoriesDictionary[categoryId] + " news:")
    news = requests.get(
        'http://localhost:9097/https://newsapi.org/v2/top-headlines?cat2egory='
        + categoriesDictionary[categoryId] + '&language=' + language +
        '&pageSize=100&apiKey=d3617fc0504c41d0a430bebf6ba1ca63')
    pageSize = re.findall('(?<=totalResults":)(.*?)(?=,"articles)',
                          str(news.text))
    print("Number of articles found for you: " + pageSize[0])

    t1 = Thread(target=showNews, args=(
        news,
        1,
    ))
    t2 = Thread(target=showNews, args=(
        news,
        2,
    ))

    t1.start()
    t2.start()


def keywordSearch():
    keywoard = input("Input the keywoard: ")
    news = requests.get(
        'http://localhost:9097/https://newsapi.org/v2/top-headlines?q=' +
        keywoard + "&language=" + language +
        "&pageSize=100&apiKey=d3617fc0504c41d0a430bebf6ba1ca63")
    pageSize = re.findall('(?<=totalResults":)(.*?)(?=,"articles)',
                          str(news.text))
    print("Number of articles found for you: " + pageSize[0])
    t1 = Thread(target=showNews, args=(
        news,
        1,
    ))
    t2 = Thread(target=showNews, args=(
        news,
        2,
    ))

    t1.start()
    t2.start()


def languagePicker():
    languages = ["de", "en", "es", "fr", "it", "nl", "no", "pt", "ru", "se"]
    languagesDictionary = {}
    print("Hello, in what language would you like your news to be?")
    for id, language in zip((range(1, len(languages) + 1)), languages):
        languagesDictionary[id] = language
        print(str(id) + ". " + language)

    languageId = int(input("Choose a language: "))
    if languageId not in range(1, 11):
        print("I didn't understand that, please pick again.")
        languagePicker()
    else:
        language = languagesDictionary[languageId]
    return language


def pickType():
    print(
        "Would like to pick a category or to search by a specific keywoard? ")
    print("1. Pick a category")
    print("2. Search by keyword")
    selectType = int(input("Choose an option: "))
    if selectType not in range(1, 3):
        print("I didn't understand that, please pick again.")
        pickType()
    else:
        if selectType == 1:
            categoryPick()
        elif selectType == 2:
            keywordSearch()


language = languagePicker()
pickType()