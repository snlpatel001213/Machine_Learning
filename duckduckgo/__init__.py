from bs4 import BeautifulSoup

import requests
import json
query = 'PARACETAMOL+TABLETS'
print 'http://duckduckgo.com/?q=' + query
response = requests.get('http://duckduckgo.com/i.js?q='+query+"&t=h_&ia=web",verify=False)
data = response.text
data = json.loads(data)
print data['results'][2]['url']