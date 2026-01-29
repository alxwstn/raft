from jinja2 import Environment, FileSystemLoader
from datetime import date
from config import config
import io

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
# }

def format_raft_html(raft_spreadsheet_data):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)

    html = template. render(config = config,
                            whiteboard_row = gen_preformatted_row(raft_spreadsheet_data['whiteboard_tracking']),
                            percent_table_row = gen_preformatted_row(raft_spreadsheet_data['percent_tracking']),
                            team_table_row = gen_preformatted_row(raft_spreadsheet_data['team_tracking'])
    )
    with open("output/RAFT_spreadsheet_analysis.html", "w") as f:
        f.write(html)

# 1&#9;2&#9;3&#9;4&#9;5&#9;6