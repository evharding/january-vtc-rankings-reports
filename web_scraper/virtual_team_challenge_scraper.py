import requests
import lxml.html as lh
import pandas as pd
import datetime
import os
import shutil

from standings_repo.repo import Session, add_rower, add_standing_sample, get_rower_by_name, check_for_sample

default_data_dir = 'vtc_standings'
time_format = '%Y-%m-%d-%H:%M:%S'
def ensure_dir(dirname):
  paths = os.path.split(dirname)
  acc = ''
  for path in paths:
    acc += path + '/'
    if not os.path.exists(acc):
      os.mkdir(acc)

def get_data(data_dirname = default_data_dir):
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
  filename = datetime.datetime.today().strftime(time_format)
  fullname = f'{data_dirname}/{filename}.csv'
  ensure_dir(data_dirname)
  df.to_csv(fullname, index=False)
  print('Done!')

def move_to_backup(data_dirname = default_data_dir, data_backup_dirname = 'vtc_standings_backup'):
  if not os.path.exists(data_backup_dirname):
      os.mkdir(data_backup_dirname)
  for filename in os.listdir(data_dirname):
    basename = os.path.basename(filename)
    to_name = f'{data_backup_dirname}/{basename}'
    from_name = f'{data_dirname}/{basename}'
    if not os.path.exists(to_name):
      shutil.copy2(from_name, to_name)
    os.remove(from_name)

def build_history(data_dirname = default_data_dir):
  for file in os.listdir(data_dirname):
    filename = f'{data_dirname}/{file}'
    print(f'Loading {filename} for insert into db...')
    new_data = pd.read_csv(filename)

    def convert_age(age):
      try:
        age = int(age)
        return age
      except:
        return None

    def convert_meters(dist):
      parsed = int(''.join(dist[:-1].split(',')))
      return parsed

    def fix_types(row):
      age = row['Age']
      dist = row['Distance']
      row['Distance'] = convert_meters(dist)
      row['Age'] = convert_age(age)
      return row
    print(new_data.head())
    print('Fixing types...')
    new_data = new_data.apply(fix_types, axis=1)
    print(new_data.head())
    date_fetched = datetime.datetime.strptime(os.path.splitext(file)[0], time_format)

    def add_standing_record(record, date_fetched):
      session = Session()
      name = record['Name']
      ranking = record['Pos.']
      sex = record['Sex']
      age = record['Age']
      rowing_club = record['Team']
      dist = record['Distance']

      rower = get_rower_by_name(session, name)
      if not rower:
        print(f'Found a new rower: {name}')
        add_rower(session, name, rowing_club, age, sex)
        rower = get_rower_by_name(session, name)
      if not check_for_sample(session, date_fetched, rower.id):
        add_standing_sample(session, date_fetched, dist, ranking, rower.id)
      session.commit()

    print('Loading into db...')
    new_data.apply(add_standing_record, axis=1, args= [date_fetched])


