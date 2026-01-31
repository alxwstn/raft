from raft_data import load_dfs, save_test_spreadsheets
from config import get_current_raft_date
from analysis import analyze
from format_output import format_raft_html

def main():
    load_dfs(False)
    raft_spreadsheet_data = analyze()
    format_raft_html(raft_spreadsheet_data)
    

if __name__ == "__main__":
    print("Running analysis for raft date {}".format(get_current_raft_date()))
    main()
    # save_test_spreadsheets()
