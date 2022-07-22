import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
  
class twitterclient(object):
    '''
    twitter class for sentiment analysis
    '''
    def __init__(self):
        '''
        class constructor
        '''
        api_key = 'dmV2vT6CQx4WgrMAQntqu0oAs'
        api_key_secret = 'yX2JF380y40xh1OvjsIn7CiDk2Wo6j3imIbI6fkO5DqVd9dyB1'
        access_token = '1475777230030606339-i8XkY6JdEHrdY6DnQRiEhxCWR6V3fB'
        access_token_secret = 'iM0iaVorgT1oXkeRn6ZyhjzHOI8eY9ao2ouveV9eCmBO8'
        try:
            self.authorize = OAuthHandler(api_key, api_key_secret)
            self.authorize.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.authorize)
        except:
            print("Error: Unable to Authenticate")
    def tweet_clean(self, tweet):
        '''
        function to clean tweet text
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", tweet).split())
    def tweet_sentiment(self, tweet):
        '''
        function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        #TextBlob object of passed tweet text
        analysis = TextBlob(self.tweet_clean(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity < 0:
            return 'negative'
        else:
            return 'neutral'
  
    def tweet_get(self, query, count = 10):
        '''
        function which will fetch the tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
  
        try:
            # twitter api is called to fetch tweets
            fetch_tweets = self.api.search_tweets(q = query, count = count)
  
            # parsing tweets one at a time
            for tweet in fetch_tweets:
                # empty dictionary to store required parameters of a tweet
                parse_tweet = {}
  
                # text of tweet is saved
                parse_tweet['text'] = tweet.text
                # sentiment of tweet is saved
                parse_tweet['sentiment'] = self.tweet_sentiment(tweet.text)
  
                # appending parsed tweet to the list tweets
                if tweet.retweet_count > 0:
                    # if tweet has retweets, then it is appended only once
                    if parse_tweet not in tweets:
                        tweets.append(parse_tweet)
                else:
                    tweets.append(parse_tweet)
  
            # return tweets which are parsed
            return tweets
  
        except Exception as e:
            print("Error : " + str(e))
 
def main():
 
    # object of the class twitterclient
    tc = twitterclient()
    # function called to get tweets
    tweets = tc.tweet_get(query = 'joe biden', count = 100)
    if tweets is not None: 
     pt = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
     print("Positive tweets percentage: {} %".format(100*len(pt)/len(tweets)))
     nt = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
     print("Negative tweets percentage: {} %".format(100*len(nt)/len(tweets)))
     print("Neutral tweets percentage: {} %".format(100*(len(tweets)-(len(nt)+len(pt)))/len(tweets)))
    
    # print tweets whichs are positive
     print("\n\nPositive tweets:")
     for tweet in pt[:5]:
        print(tweet['text'])

    # print tweets which are negative
     print("\n\nNegative tweets:")
     for tweet in nt[:5]:
        print(tweet['text'])
  
if __name__ == "__main__":
    # calling main function
    main() 