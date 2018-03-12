from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sentiment_mod as s

consumer_key = 'q0r3SM2mH1qQr8gbenXkSeCDW'
consumer_secret = 'JZ7Tgy3HGqBrciyo71A4IIMldrCtj3ydKtwjZHaQhKynOInnQq'
access_token = '2173884223-H8h1i3J45pluZelpN8BuwYdqI195sOLHc7HRrzG'
access_token_secret = 'jAn0XNDXjwnRpjXbSENKVpZDkcpfRbJceowT1xD52F70Z'



class listener(StreamListener):

    def on_data(self, data):
        try:
            all_data = json.loads(data)
            tweet = all_data['text']
            value,conf = s.sentiment(tweet)
            print(tweet,'Value is',value,'confidence level is',conf)
            if conf*100>=80:
                output = open('twitter-out.txt','a')
                output.write(value)
                output.write('\n')
                output.close()
            return True
        except:
            return True
            
    def on_error(self, status):
        print(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Narendra Modi"])
