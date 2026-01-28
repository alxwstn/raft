import pandas as pd
from raft_data import load_dfs, get_postraft_df, get_preraft_df
from config import get_current_raft_date

def main():
    load_dfs(True)
    print("PRE RAFT")
    print(get_preraft_df().head(2))
    print("POST RAFT")
    print(get_postraft_df().head(2))

if __name__ == "__main__":
    print("Running analysis for raft date {}".format(get_current_raft_date))
    main()

