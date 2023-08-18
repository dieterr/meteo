#!/usr/bin/python

import requests
response = requests.get('http://196.168.0.206/')
print (response.status_code)
print (response.content)



#import urllib.request as urllib
##import urllib2
#req = urllib.Request('http://196.168.0.206/')
##response = urllib.urlopen(req)
#response = urllib.urlopen(req)
#print(type(response))
#page = response.read()
##page = urllib.request.urlopen('http://196.168.0.206/')
##print(page)
