from jinja2 import Environment, FileSystemLoader
from config import config
from raft_data import get_postraft_df
import logging


template_name = "RAFT_output_template.html"

def gen_preformatted_row(row_list):
    return "&#9;".join(row_list)
    
# given a dictionary of spreadsheet data, generate an html page
# that contains config info and row data ready for copy into the
# destination spreadsheets.
# input format
#  {
#         "whiteboard_tracking": List[str],
#         "percent_tracking": List[str],
#         "team_tracking": List[str]
#         'team_tracking_debug_dfs': {
#           'todays_raft_df': pandas.DataFrame,
#           'grand_total_trash_before_raft_df': pandas.DataFrame,
#           'grand_total_trash_after_raft_df': pandas.DataFrame,
#           'since_last_raft_df': pandas.DataFrame,
#           'since_and_including_last_raft': pandas.DataFrame
#          }
# }

def format_raft_html(raft_spreadsheet_data):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    team_today_raft_table_html = ''
    team_since_last_raft_table_html = ''
    try:
        team_today_raft_table_html = raft_spreadsheet_data['team_tracking_debug_dfs']['todays_raft_df'][['Longitude','Site Name ','Category','uid','reg_datetime','Bags of Trash']].to_html(table_id='team_today_raft')
        team_since_last_raft_table_html = raft_spreadsheet_data['team_tracking_debug_dfs']['since_last_raft_df'][['Longitude','Site Name ','Category','uid','reg_datetime','Bags of Trash']].to_html(table_id='team_since_last_raft')
        team_since_and_including_last_raft_table_html = raft_spreadsheet_data['team_tracking_debug_dfs']['since_and_including_last_raft'][['Longitude','Site Name ','Category','uid','reg_datetime','Bags of Trash']].to_html(table_id='since_and_including_last_raft')
    except Exception as e:
        logging.exception(e)
        logging.warning('Failed to generate Team Tracking Detailed output. Manually recheck.')

    html = template. render(config = config,
                            whiteboard_row = gen_preformatted_row(raft_spreadsheet_data['whiteboard_tracking']),
                            percent_table_row = gen_preformatted_row(raft_spreadsheet_data['percent_tracking']),
                            team_table_row = gen_preformatted_row(raft_spreadsheet_data['team_tracking']),
                            team_today_raft = team_today_raft_table_html,
                            team_since_last_raft = team_since_last_raft_table_html,
                            team_since_and_including_last_raft = team_since_and_including_last_raft_table_html
    )
    with open("output/RAFT_spreadsheet_analysis.html", "w") as f:
        f.write(html)

def format_mappler_csv():
    mappler_df = get_postraft_df()
    mappler_df.to_csv('output/Mappler.csv',index=False)