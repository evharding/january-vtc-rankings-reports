import report_generation.virtual_team_challenge_reporter as reporter
import web_scraper.virtual_team_challenge_scraper as scraper

data_dir = './data/vtc_standings'
backup_dir = './data/vtc_standings_backup'
reporting_dir ='./data/reports'

scraper.get_data(data_dir)
reporter.graphs(data_dir, reporting_dir)
reporter.reports(data_dir, reporting_dir)
scraper.move_to_backup(data_dir, backup_dir)