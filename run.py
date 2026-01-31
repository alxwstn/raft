from raft_data import load_dfs, DataSource, save_test_spreadsheets
from config import get_current_raft_date
from analysis import analyze
from format_output import format_raft_html

def main():
    # DataSource options: LOCAL_EXCEL, LOCAL_CSV, DRIVE_EXCEL
    load_dfs(DataSource.DRIVE_EXCEL)
    raft_spreadsheet_data = analyze()
    format_raft_html(raft_spreadsheet_data)
    

if __name__ == "__main__":
    print("Running analysis for raft date {}".format(get_current_raft_date()))
    main()
