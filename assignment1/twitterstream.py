import oauth2 as oauth
import urllib2 as urllib
import os.path as osp
import ConfigParser
import StringIO
import sys

# See assignment1.html instructions or README for how to get these credentials

# Load file with twitter info
twitter_api_path = osp.abspath(osp.join(osp.dirname(osp.dirname(osp.abspath(__file__))), 'twitter_api'))

if not osp.exists(twitter_api_path):
  print 'ERROR: could not find Twitter API file: ' + twitter_api_path
  sys.exit(1)


ini_str = '[root]\n' + open(twitter_api_path, 'r').read()
ini_fp = StringIO.StringIO(ini_str)
config = ConfigParser.RawConfigParser()
config.readfp(ini_fp)


api_key = config.get('root', 'api_key')
api_secret = config.get('root', 'api_secret')
access_token_key = config.get('root', 'access_token_key')
access_token_secret = config.get('root', 'access_token_secret')

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    print line.strip()

if __name__ == '__main__':
  fetchsamples()
