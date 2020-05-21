import csv
import time

def preProcessTweets(fileLink):

    corpus = []

    with open(fileLink, 'r') as csvfile:
        lineReader = csv.reader(csvfile,delimiter=';')
        for row in lineReader:
            print(row)
            #corpus.append({"tweet_id":row[2], "label":row[1], "topic":row[0]})

preProcessTweets("dengvaxia.csv")
