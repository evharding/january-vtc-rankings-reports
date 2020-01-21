import requests
import lxml.html as lh
import pandas as pd
import datetime
import os

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
dirname = 'vtc-standings'
filename = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
fullname = f'{dirname}/{filename}.csv'
if not os.path.exists(dirname):
  os.mkdir(dirname)
df.to_csv(fullname, index=False)
print('Done!')