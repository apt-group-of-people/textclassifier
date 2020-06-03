import csv
from tweetcleaner import tweet_cleaner, preprocess_tweet

def getData(fileName):
    with open(fileName, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        with open('newtestdata.txt', 'w+', encoding='utf-8') as new_file:
            for x in csv_reader:
                new_file.write(f'{preprocess_tweet(x["tweet"])}\t{x["label"]}\n')

getData('./kaggle/train.csv')
