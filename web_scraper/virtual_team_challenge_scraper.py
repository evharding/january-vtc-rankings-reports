import requests
import lxml.html as lh
import pandas as pd
import datetime
import os
import shutil

def ensure_dir(dirname):
  paths = os.path.split(dirname)
  acc = ''
  for path in paths:
    acc += path + '/'
    if not os.path.exists(acc):
      os.mkdir(acc)

def get_data(data_dirname = 'vtc_standings'):
  url='https://log.concept2.com/challenges/vtc/2020/individuals'
  #Create a handle, page, to handle the contents of the website
  page = requests.get(url)
  #Store the contents of the website under doc
  doc = lh.fromstring(page.content)
  #Parse data that are stored between <tr>..</tr> of HTML
  tr_elements = doc.xpath('//tr')
  table = [[td.text_content() for td in tr] for tr in tr_elements]

  df = pd.DataFrame.from_records(table[1:], columns=table[0])

  print('Received standings, writing to csv...')
  filename = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
  fullname = f'{data_dirname}/{filename}.csv'
  ensure_dir(data_dirname)
  df.to_csv(fullname, index=False)
  print('Done!')

def move_to_backup(data_dirname = 'vtc_standings', data_backup_dirname = 'vtc_standings_backup'):
  if not os.path.exists(data_backup_dirname):
      os.mkdir(data_backup_dirname)
  for filename in os.listdir(data_dirname):
    basename = os.path.basename(filename)
    to_name = f'{data_backup_dirname}/{basename}'
    from_name = f'{data_dirname}/{basename}'
    if not os.path.exists(to_name):
      shutil.copy2(from_name, to_name)
    os.remove(from_name)