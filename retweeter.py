from twython import Twython, TwythonStreamer

APP_KEY = ''
APP_SECRET = ''

twitter = Twython(APP_KEY, APP_SECRET)
auth = twitter.get_authentication_tokens()

twitter = Twython(APP_KEY, APP_SECRET,
                  auth['oauth_token'], auth['oauth_token_secret'])

print "Go to: " + auth['auth_url']
oauth_verifier = raw_input("Enter PIN: ")

tokens = twitter.get_authorized_tokens(oauth_verifier)

OAUTH_TOKEN = tokens['oauth_token']
OAUTH_TOKEN_SECRET = tokens['oauth_token_secret']

print "APP_KEY           : " + APP_KEY
print "APP_SECRET        : " + APP_SECRET
print "OAUTH_TOKEN       : " + OAUTH_TOKEN
print "OAUTH_TOKEN_SECRET: " + OAUTH_TOKEN_SECRET


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code
        print data

stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track='twitter')
