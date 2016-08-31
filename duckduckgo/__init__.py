from bs4 import BeautifulSoup

import requests
import json
import re
import urllib
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
site = urllib.urlopen('http://duckduckgo.com/html/?q=rustom+movie', context=ctx)
data = site.read()
parsed = BeautifulSoup(data)
# print parsed
print parsed.findAll('div', {'class': 'result__extras__url'})[3].a['href']
