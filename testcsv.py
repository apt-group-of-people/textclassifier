import csv

def getData(fileName):
    with open(fileName, 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for x in csv_reader:
            if x['sentiment'] != 'negative' or x['sentiment'] != 'positive' or x['sentiment'] != 'neutral':
                print('error')
            else:
                print(f"TWEET: {x['text']}, SENTIMENT: {x['sentiment']}")

getData('./data/du30-administration-labeled.csv')
