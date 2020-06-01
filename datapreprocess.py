#
# Preprocess test
#
import random
import nltk

def createFile(posFile, negFile, neuFile):
    with open('all_tweet.txt', 'w') as all_file:
        with open(negFile, 'r') as neg_file:
            for data in neg_file:
                all_file.write(f'{data.strip()}\tneg\n')
                
        with open(neuFile, 'r') as neu_file:
            for data in neu_file:
                all_file.write(f'{data.strip()}\tneu\n')
                
        with open(posFile, 'r') as pos_file:
            for data in pos_file:
                all_file.write(f'{data.strip()}\tpos\n')

def getFile(data):
    all_data = []
    with open(data, 'r') as file:
        for line in file:
            cat = line.strip().split('\t')
            all_data.append(([x for x in cat[0].split()],cat[1]))

    random.shuffle(all_data)

    all_words = []
    for w in all_data:
        for x in w[0]:
            all_words.append(x)
    all_words = nltk.FreqDist(all_words)
    #print(all_words.most_common(100))
    word_features = list(all_words.keys())[:3000]
    #print(len(list(all_words.keys())))

    return all_data, all_words, word_features
        
def find_features(data, wfeatures):
    words = set(data)
    features = {}
    for w in wfeatures:
        features[w] = (w in words)

    return features

def classify_train(fileName, algo):
    all_data, all_words, word_features = getFile(fileName)
    featuresets = [(find_features(tweet, word_features), sent) for (tweet, sent) in all_data]
    training_set = featuresets[:150]
    testing_set = featuresets[150:]
    classifier = []
    if algo == 'naive':
        classifier = nltk.NaiveBayesClassifier.train(training_set)
    elif algo == 'decision':
        classifier = nltk.classify.DecisionTreeClassifier.train(training_set,
                                                                entropy_cutoff=0,
                                                                support_cutoff=0)
        
    print(f"{algo} Bayes Acc:", (nltk.classify.accuracy(classifier, testing_set))*100)
    #classifier.show_most_informative_features(15)
    #print(testing_set[0][0])
    print(classifier.labels())
    #test_probability = classifier.prob_classify(testing_set[0][0])
    test_predict = classifier.classify(testing_set[0][0])
    print(test_predict)
    #for sample in test_probability.samples():
        #print(f'{sample}: {test_probability.prob(sample)}')

if __name__== '__main__':
    #createFile('./cleanedtweets-pos.txt','./cleanedtweets-neg.txt','./cleanedtweets-neu.txt')
    classify_train('all_tweet.txt', 'decision')










