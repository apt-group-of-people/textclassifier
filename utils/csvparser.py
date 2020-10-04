import csv
from tweetcleaner import preprocess_tweet

def getData(fileName):
    with open(fileName, 'r', encoding='latin-1') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        with open('newtestdata.txt', 'w+', encoding='utf-8') as new_file:
            for x in csv_reader:
                #print(x)
                new_file.write(f'{preprocess_tweet(x["SentimentText"])}\t{x["Sentiment"]}\n')

getData('../kaggle_data/train.csv')
