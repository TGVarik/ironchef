import json

with open('ironchef2.json', 'r') as f:
  data = json.load(f)
urls = []
for ep in data:
  for link in ep['links']:
    urls.append(link['url'])
with open('ironchef.txt', 'w') as f:
  f.writelines(['{:s}\n'.format(u) for u in urls])