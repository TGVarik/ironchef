# coding=utf-8
from __future__ import unicode_literals
from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from bs4 import BeautifulSoup
from json import dumps
import requests

episodes = []
driver = webdriver.Chrome()
#driver.set_window_size(1440,900)
xp = driver.find_element_by_xpath
xps = driver.find_elements_by_xpath


def parse_episode(id):
  driver.get('http://filehouse.ironcheffans.info/index.php?act=view&id={:d}'.format(id['id']))
  doc = BeautifulSoup(driver.page_source)
  ep = {
    'id': id['id'],
    'kind': id['kind']
  }
  rows = doc.body.find_all('table')[3].tbody.find_all('tr')
  for row in rows:
    tds = row.find_all('td')
    if len(tds) < 2:
      ep['title'] = tds[0].text.strip()
    elif tds[0].text.strip() == 'Description:':
      ep['desc'] = tds[1].text.strip()
    elif tds[0].text.strip() == 'Judges:':
      ep['judges'] = tds[1].text.strip()
    elif tds[0].text.strip() == 'Iron Chef:':
      ep['ironchef'] = tds[1].text.strip()
    elif tds[0].text.strip() == 'Theme Ingredient:':
      ep['ingredient'] = tds[1].text.strip()
    elif tds[0].text.strip() == 'Challenger:':
      ep['challenger'] = tds[1].text.strip()
    elif tds[0].text.strip() == 'Language:':
      ep['language'] = tds[1].text.strip()
    elif tds[0].text.strip() == 'Subtitles:':
      ep['subtitles'] = tds[1].text.strip()
    elif tds[0].text.strip() == 'O. A.:':
      ep['airdate'] = tds[1].text.strip().split(', ')[0].split(' and ')[0]
    elif tds[0].text.strip() in ['Date Added:', 'Last Download:', 'Downloads:', 'Rating:', 'Iron Chef Wiki Page:', 'Episode Review:']:
      pass
    else:
      raise Exception('Unaccounted-for data: {:s}'.format(tds[0]))
  r = requests.get('http://filehouse.ironcheffans.info/index.php?act=download&id={:d}'.format(ep['id']), allow_redirects=False)
  url = BeautifulSoup(r.content).body.find('a').attrs['href']
  episodes.append(url)
  return ep

ids = []
eps = []

driver.get('http://filehouse.ironcheffans.info')
login = xp('/html/body/table[2]/tbody/tr/td[2]/a[2]')
if login.text == 'Login':
  login.click()
  xp('/html/body/form/table/tbody/tr[2]/td[2]/input').send_keys('tgvarik')
  xp('/html/body/form/table/tbody/tr[3]/td[2]/input').send_keys('zwMn2z4i&gpsu6,sF9xm')
  xp('/html/body/form/table/tbody/tr[4]/td/input').click()
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/table[4]/tbody/tr[3]/td[1]/a')))

categories = [
  {'id': 1, 'kind': 'eng'},
  {'id': 3, 'kind': 'jpn'},
  {'id': 4, 'kind': 'special'}
]
for cat in categories:
  driver.get('http://filehouse.ironcheffans.info/index.php?act=category&id={:d}'.format(cat['id']))
  while True:
    doc = BeautifulSoup(driver.page_source)
    anchors = [el for list in [doc.select('tr.row1 a'), doc.select('tr.row2 a')] for el in list]
    for anchor in anchors:
      url = anchor.attrs['href']
      id = int(url.split('id=')[-1])
      ids.append({'id': id, 'kind': cat['kind']})
    if xps('/html/body/div[1]/a')[-1].text != '»»':
      break
    else:
      xps('/html/body/div[1]/a')[-1].click()
print(len(ids))

for id in ids:
  ep = parse_episode(id)
  eps.append(ep)
print(len(eps))
with open('ironchef.json', 'w') as f:
  f.write(dumps(eps))
with open('ironchef.txt', 'w') as f:
  f.writelines(episodes)