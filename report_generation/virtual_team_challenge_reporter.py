import report_generation.vtc_reporting.make_report as rprt
import pandas as pd
import datetime
import os

def reports(data_dirname = 'vtc_standings', reporting_dir ='reports'):
  report_files = []
  for file in os.listdir(data_dirname):
    report_date = os.path.splitext(file)[0]
    # Get all the nbc-ers as the dataframe, with distances as integer values
    rankings = pd.read_csv(f'{data_dirname}/{file}')
    nbcers = rankings.where(rankings['Team'] == 'Narragansett Boat Club').dropna()
    saved_report = rprt.make_stats(nbcers, reporting_dir, report_date)
    report_files.append(saved_report)
  return report_files

def graphs(data_dirname = 'vtc_standings', reporting_dir ='reports'):
  graph_files = []
  for file in os.listdir(data_dirname):
    report_date = os.path.splitext(file)[0]
    # Get all the nbc-ers as the dataframe, with distances as integer values
    rankings = pd.read_csv(f'{data_dirname}/{file}')
    nbcers = rankings.where(rankings['Team'] == 'Narragansett Boat Club').dropna()
    saved_graphs = rprt.make_graphs(nbcers, reporting_dir, report_date)
    graph_files.extend(saved_graphs)
  return graph_files