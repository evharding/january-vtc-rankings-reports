import vtc_reporting.scatter_plots as scatter
import os

def ensure_dir(dirname):
  paths = os.path.split(dirname)
  acc = ''
  for path in paths:
    acc += path + '/'
    if not os.path.exists(acc):
      os.mkdir(acc)

def convert_meters(dist):
  parsed = int(''.join(dist[:-1].split(',')))
  return parsed

def for_current_set(nbcers, reporting_dir, report_date):
  # Ensure that we have a directory to save the report
  dated_report_dir = f'{reporting_dir}/{report_date}'
  ensure_dir(dated_report_dir)

  # Make sure the fields we expect to be numbers are numbers
  nbcers['Distance'] = nbcers['Distance'].apply(convert_meters)
  nbcers['Age'] = nbcers['Age'].astype('int')
  print(f'\n=================== {report_date} ===================')
  print(nbcers.head())

  ladies = nbcers.where(nbcers['Sex'] == 'F' )
  gents = nbcers[1::].where(nbcers['Sex'] == 'M')
  gents_with_charlie = nbcers.where(nbcers['Sex'] == 'M')
  under40 = nbcers.where(nbcers['Age'] < 40)
  middle_age = nbcers.where((nbcers['Age'] >= 40) & (nbcers['Age'] < 65))
  over65 = nbcers.where(nbcers['Age'] >= 65)

  scatter.make_scatter(under40.dropna(), 'Under 40 Crowd', f'{dated_report_dir}/youngfolks.png')
  scatter.make_scatter(middle_age.dropna(), '40 to 65 Crowd', f'{dated_report_dir}/middlefolks.png')
  scatter.make_scatter(over65.dropna(), 'The 65+ Crowd', f'{dated_report_dir}/oldcrowd.png')
  scatter.make_scatter(gents.dropna(), 'Just The Boys', f'{dated_report_dir}/just-the-boys.png')
  scatter.make_scatter(ladies.dropna(), 'Just The Girls', f'{dated_report_dir}/just-the-girls.png')

  # get some stats:
  tmean = round(nbcers['Distance'].mean())
  ttotal = nbcers['Distance'].sum()
  lmean = round(ladies['Distance'].mean())
  ltotal = ladies['Distance'].sum()
  gwc_mean = round(gents_with_charlie['Distance'].mean())
  gwc_total = gents_with_charlie['Distance'].sum()
  gmean = round(gents['Distance'].mean())
  gtotal = gents['Distance'].sum()

  u40mean = round(under40['Distance'].mean())
  u40total = under40['Distance'].sum()
  middle_mean = round(middle_age['Distance'].mean())
  middle_total = middle_age['Distance'].sum()
  old_mean = round(over65['Distance'].mean())
  old_total = over65['Distance'].sum()


  with open(f'{dated_report_dir}/stats.txt', 'w') as f:
    f.write(f'{report_date}')
    f.write(f'\n\n{"":<19}{"Mean":>10}{"Total":>16}')
    f.write(f'\n{"All:":<19}{tmean:>10,}m{ttotal:>15,}m')
    f.write(f'\n{"Ladies:":<19}{lmean:>10,}m{ltotal:>15,}m')
    f.write(f'\n{"Gents:":<19}{gmean:>10,}m{gtotal:>15,}m')
    f.write(f'\n{"U40:":<19}{u40mean:>10,}m{u40total:>15,}m')
    f.write(f'\n{"40 - 65 Crowd:":<19}{middle_mean:>10,}m{middle_total:>15,}m')
    f.write(f'\n{"65+ Crowd:":<19}{old_mean:>10,}m{old_total:>15,}m')
    f.write(f'\n{"-"*46}')
    f.write(f'\n{"(Gents w/Charlie):":<19}{gwc_mean:>10,}m{gwc_total:>15,}m')
