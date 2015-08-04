import json
import requests
import requests.adapters
from bs4 import BeautifulSoup

session = requests.Session()
session.mount("http://", requests.adapters.HTTPAdapter(max_retries=5))
session.mount("https://", requests.adapters.HTTPAdapter(max_retries=5))



with open('ironchef.json', 'r') as f:
  data = json.load(f)
total = len(data)
i = 0
for ep in data:
  i += 1
  print('{:03d}/{:03d}'.format(i, total))
  ep['links'] = []
  r = session.get('http://filehouse.ironcheffans.info/index.php?act=mirror&id={:d}'.format(ep['id']))
  if r.content == '':
    links=['http://filehouse.ironcheffans.info/index.php?act=download&id={:d}'.format(ep['id'])]
  else:
    links = BeautifulSoup(r.content).body.find_all('table')[3].find_all('a')
  for link in links:
    follow = None
    if isinstance(link, basestring):
      follow = link
      kind = 'Download File'
    elif link.text.strip() != 'Watch Video':
      follow = link.attrs['href']
      kind = link.text.strip()
    if follow is not None:
      r2 = session.get(follow, allow_redirects=False)
      url = BeautifulSoup(r2.content).body.find('a').attrs['href']
      ep['links'].append({'title': kind, 'url': url})
with open('ironchef2.json', 'w') as f:
  json.dump(data, f)

