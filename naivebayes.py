import random
import nltk
from nltk.corpus import movie_reviews

with open("tweets.txt", 'r') as file:
        for x in file.readlines():
                print(x)

# documents = [(list(movie_reviews.words(fileid)), category)
#              for category in movie_reviews.categories()
#              for fileid in movie_reviews.fileids(category)]

# random.shuffle(documents)

# print(documents[1])
