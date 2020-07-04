import tweepy
from PyQt5.QtCore import Qt, QThread, pyqtSignal



class twitter_api(QThread):
    taskFinished = pyqtSignal()
    def __init__(self,user_ID,tweets_count, consumer_key='1zymhtpFutBUusEw4mmrrByb5',
                 consumer_secret='vR4lh77ih8VVRL3oDIvYyvhGR3kedM6Uw20nGlceiDnVIQ8LYF',
                 access_token='1258372102366912513-hS8VMVfwn22w3brCol5Lm205VkXdtY',
                 access_token_secret='c6CYBJ9C6KxtoSCFDbajDS3tzMuZsAZrFnqil7CAamvJW'
                 ):
        """
        accessing to tweepy API by insert tokens
        :param user_ID:
        :param tweets_count:
        :param consumer_key:
        :param consumer_secret:
        :param access_token:
        :param access_token_secret:
        """
        super(twitter_api, self).__init__()
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)
        self.user_ID = user_ID
        self.tweets_count = tweets_count


    def run(self):
        self.is_run = True
        #self.tweets_count = tweets_count
        self.final_tweets_count = self.tweets_count
        #self.user_id = user_ID
        try:
            self.tweets = self.api.user_timeline(screen_name=self.user_ID, count=self.tweets_count, include_rts=False,tweet_mode='extended')

        except tweepy.TweepError as err:
            self.taskFinished.emit()
            return
        self.all_tweets_list = []
        for tweet in self.tweets[:self.tweets_count]:
            self.all_tweets_list.append(str(tweet._json['id']) + " " + tweet._json['full_text'] + '\n')
        self.temp_count=self.tweets_count-len(self.all_tweets_list)
        print(self.temp_count)
        for i in range(0,5):#need to fix because increase tweets list x5
            if self.temp_count!=0:
                self.tweets_count=self.tweets_count+5
                self.all_tweets_list=[]
                self.tweets = self.api.user_timeline(screen_name=self.user_ID, count=self.tweets_count, include_rts=False,
                                    tweet_mode='extended')
                for tweet in self.tweets[:self.tweets_count]:
                    self.all_tweets_list.append(str(tweet._json['id']) + " " + tweet._json['full_text'] + '\n')
                self.temp_count = self.tweets_count - len(self.all_tweets_list)
                if self.temp_count == self.final_tweets_count:
                    break
        self.taskFinished.emit()