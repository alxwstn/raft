from jinja2 import Environment, FileSystemLoader
from datetime import date
import io

template_name = "RAFT_output_template.html"

def go():
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)

    html = template. render(name="World")
    with open("output/RAFT_spreadsheet_analysis_{}.html".format(date.today().isoformat()), "w") as f:
        f.write(html)
