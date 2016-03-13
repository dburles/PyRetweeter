#!/usr/bin/env python
from twython import Twython, TwythonStreamer
import ConfigParser

CONFIG_FILE = 'config.cfg'

config = ConfigParser.RawConfigParser()
config.read(CONFIG_FILE)

app_key = config.get('oauth', 'app_key')
app_secret = config.get('oauth', 'app_secret')
oauth_token = config.get('oauth', 'oauth_token')
oauth_token_secret = config.get('oauth', 'oauth_token_secret')
track = config.get('general', 'track')

if not oauth_token and not oauth_token_secret:
    twitter = Twython(app_key, app_secret)
    auth = twitter.get_authentication_tokens()

    twitter = Twython(app_key, app_secret,
                      auth['oauth_token'], auth['oauth_token_secret'])

    print "Go to: " + auth['auth_url']
    oauth_verifier = raw_input("Enter PIN: ")

    tokens = twitter.get_authorized_tokens(oauth_verifier)

    oauth_token = tokens['oauth_token']
    oauth_token_secret = tokens['oauth_token_secret']

    config.set('oauth', 'oauth_token', oauth_token)
    config.set('oauth', 'oauth_token_secret', oauth_token_secret)

    with open(CONFIG_FILE, 'wb') as configfile:
        config.write(configfile)

print "app_key           : " + app_key
print "app_secret        : " + app_secret
print "oauth_token       : " + oauth_token
print "oauth_token_secret: " + oauth_token_secret

twitter = Twython(app_key, app_secret,
                  oauth_token, oauth_token_secret)


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data and not data['text'][0:2] == 'RT':
            print data['text'].encode('utf-8')
            print "Retweeting.. " + data['id_str']
            twitter.retweet(id=data['id'])

    def on_error(self, status_code, data):
        print status_code
        print data

        self.disconnect()

stream = MyStreamer(app_key, app_secret,
                    oauth_token, oauth_token_secret)
stream.statuses.filter(track=track)
