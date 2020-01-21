#!~/anaconda3/bin/python
import vtc_reporting.make_report as rprt
import pandas as pd
import datetime
import os

reporting_dir = 'reports'

for file in os.listdir('./vtc-standings'):
  report_date = os.path.splitext(file)[0]
  # Get all the nbc-ers as the dataframe, with distances as integer values
  rankings = pd.read_csv(f'./vtc-standings/{file}')
  nbcers = rankings.where(rankings['Team'] == 'Narragansett Boat Club').dropna()
  rprt.for_current_set(nbcers, reporting_dir, report_date)