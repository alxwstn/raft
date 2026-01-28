import configparser
import datetime

full_config = configparser.ConfigParser()
full_config.read('config.ini')

# careful, everything is returned as a string!
config = full_config['raft']

# helper methods return iso date strings as parsed date objects
def get_current_raft_date():
    return datetime.date.fromisoformat(config["current_raft_date"])

def get_last_raft_date():
    return datetime.date.fromisoformat(config["last_raft_date"])