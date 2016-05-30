__author__ = 'trevorlindsay'


import urllib
import urlparse
import hmac
import hashlib
import base64


BASE_URL = 'https://maps.googleapis.com/maps/api/streetview?'
PARAMS = {'size': '640x400',
          'location': None,
          'pitch': 0,
          'fov': 90}


def getImage(location, filename, creds, **kwargs):

    global BASE_URL, PARAMS
    base_url = BASE_URL
    params = PARAMS

    params['location'] = location
    params['key'] = creds.get('key')
    secret = creds.get('secret')

    for arg, value in kwargs.iteritems():
        print arg, value


    for paramName, paramValue in params.iteritems():
        base_url = '{0}&{1}={2}'.format(base_url, paramName, paramValue)

    base_url = base_url.replace(' ', '%20')
    url = addSignature(base_url, secret)

    print url
    urllib.urlretrieve(url, filename+'.jpg')


def addSignature(input_url, secret):

    print input_url
    url = urlparse.urlparse(input_url)
    url_to_sign = url.path + "?" + url.query

    decoded_key = base64.urlsafe_b64decode(secret)
    signature = hmac.new(decoded_key, url_to_sign, hashlib.sha1)
    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    print encoded_signature
    return input_url + '&signature=' + encoded_signature


def getCredentials(filename='credentials.cfg'):

    with open(filename) as f:
        creds = [tuple(cred.strip().split('::')) for cred in f.readlines()]

    return {cred[0]:cred[1] for cred in creds}


credentials = getCredentials()
location = 'Stone Mountain, GA'

getImage(location, 'stone_mountain', credentials)