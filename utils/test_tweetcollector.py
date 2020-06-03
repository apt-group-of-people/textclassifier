import GetOldTweets3 as got 

tweetCriteria = got.manager.TweetCriteria()\
    .setQuerySearch("#Dengvaxia")\
    .setSince("2020-01-01")\
    .setUntil("2020-04-27")\
    .setTopTweets(True)\
    .setMaxTweets(10)
    

def SaveData(data):
    a = open('tweets.txt', 'w')
    a.write(data)
    a.close
    

tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
print(tweet)