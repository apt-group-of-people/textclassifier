import random
import nltk
import sys
from tweetcleaner import preprocess_tweet
from sklearn.svm import LinearSVC
import pickle
from tkinter import *


LARGE_FONT = ("Verdana", 12, "bold")
BUTTON_FONT = ("Verdana", 10)

update = []
        
def find_features(data, wfeatures):
    words = set(data)
    features = {}
    for w in wfeatures:
        features[w] = (w in words)

    return features

def getFile(data, word_use):
    all_data = []
    print('Preprocessing Data...')
    update.append('Preprocessing Data...')
    with open(data, 'r', encoding="utf-8") as file:
        for line in file:
            cat = line.strip().split('\t')
            if len(cat) <= 1:
                continue
            all_data.append(([x for x in cat[0].split(' ')],cat[1]))
    print(f'There are {len(all_data)} usable lines of tweets...\n')
    update.append(f'There are {len(all_data)} usable lines of tweets...\n')
    
    random.shuffle(all_data)

    all_words = []
    print(f'Counting words...')
    update.append(f'Counting words...')
    for w in all_data:
        for x in w[0]:
            all_words.append(x.lower())
    all_words = nltk.FreqDist(all_words)
    print(f'\n100 most common words:\n{all_words.most_common(100)}\n')
    word_features = list(all_words.keys())[:word_use]
    update.append(f'There are currently {len(list(all_words.keys()))} unique words...')
    print(f'There are currently {len(list(all_words.keys()))} unique words...')
    print(f'Using only {word_use} words...\n')
    update.append(f'Using only {word_use} words...\n')

    return all_data, word_features

# The file path, number of words to be used, alogrithm
def classify_train(fileName, word_use, algo='naive'):
    print(f'Training {fileName} using {algo} algorithm...')
    update.append(f'Training {fileName} using {algo} algorithm...')
    all_data, word_features = getFile(fileName, word_use)
    print(f'Creating features...')
    update.append(f'Creating features...')
    featuresets = [(find_features(tweet, word_features), sent) for (tweet, sent) in all_data]
    training_set = featuresets[:word_use//2]
    testing_set = featuresets[word_use//2:]
    classifier = []
    print('Data currently being trained...\n')
    update.append('Data currently being trained...\n')
    if algo == 'naive':
        classifier = nltk.NaiveBayesClassifier.train(training_set)
    elif algo == 'decision':
        classifier = nltk.classify.DecisionTreeClassifier.train(training_set,
                                                                entropy_cutoff=0,
                                                                support_cutoff=0)
    elif algo == 'svm':
        classifier = nltk.classify.SklearnClassifier(LinearSVC()).train(training_set)
    acc = (nltk.classify.accuracy(classifier, testing_set))*100
    update.append(f"Classifier accuracy: {acc}")
    print(f"Classifier accuracy: {acc}")
    print(f"Training finished!")
    update.append(f"Training finished!")
    full_data = {"classifier": classifier, "features": word_features}
    print(update)

    return full_data, acc, update
    #classifier_outfile = open('pickled_classify.pickle', 'wb')
    #pickle.dump(full_data, classifier_outfile)
    #classifier_outfile.close()
    
    #classifier.show_most_informative_features(15)
    #print(classifier.labels())
    #test_probability = classifier.prob_classify(testing_set[0][0])
    #test_predict = classifier.classify(testing_set[0][0])
    #print(test_predict)
    #for test_tweet, test_sent in testing_set:
    #    print(f"{' '.join(list(test_tweet.keys()))}")
    #    print(f"Correct Sentiment: {test_sent}")
    #   print(f"Predicted Sentiment: {classifier.classify(test_tweet)}\n\n")
    #for sample in test_probability.samples():
        #print(f'{sample}: {test_probability.prob(sample)}')

def classify_data(classify, tweet):
    cleaned_tweet = preprocess_tweet(tweet)
    tweet_feature = find_features(tweet, classify['features'])
    prediction = classify['classifier'].classify(tweet_feature)
    return prediction

#if __name__== '__main__':
    #test = classify_train('new_data/newtestdata.txt',300,'naive')
    #pickle_in = open("pickled_classify.pickle","rb")
    #classifier_data = pickle.load(pickle_in)
    #test = classify_data(classifier_data, "@user supposedly taunton didn't cross paths w/ hitchens during his last year. just another religion claiming the dead.")
    #print(test)
#report = Tk()
#termf = Frame(report, height=200, width=300, bg="#4285f4")
#report.geometry('300x200')
#report.configure(bg='black')
#report.resizable(0, 0)
#termf.pack(fill=BOTH)
#name = Label(termf, text="Training Result", fg="white", bg="#4285f4", font=LARGE_FONT)
#name.pack()

#dataFrame = Frame(report, bg="black")
#dataFrame.pack(side=LEFT, anchor="nw", padx=(5, 0))

#i = 1
#for x in update:
#    lb = Label(dataFrame, text=x, fg="white", bg="black")
#    lb.grid(row=i, column=1)
#    i += 1
#report.mainloop()








