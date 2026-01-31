import io
import os
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from config import config
import datetime
import olefile
import xlrd
import logging
import sys

# There is a better way to do this
preraft_df: pd.DataFrame = None
postraft_df: pd.DataFrame = None
def get_preraft_df():
    # preraft_df
    return preraft_df

def get_postraft_df():
    # preraft_df
    return postraft_df

# pandas df conversion things
def convert_bags(x):
    try:
        return int(x)
    except:
        return 0
    
def convert_regdatetime(x):
    return datetime.date.fromisoformat(x[0:10])

dtype_map = {
    'Longitude': float
}

converters_map = {
    'Bags of Trash': convert_bags,
    'reg_datetime': convert_regdatetime
}
# load the raft spreadsheet into a dataframe with the correct datatypes
# see https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html#pandas.read_excel
def load_raft_spreadsheet(reference, info=''):
    try:
        return pd.read_excel(reference, dtype=dtype_map, converters=converters_map)
    except xlrd.compdoc.CompDocError:
        logging.warning('{}: Falling back to ole to handle Compound File Binary. See https://stackoverflow.com/a/60416081'.format(info))
        ole = olefile.OleFileIO(reference)
        if ole.exists('Workbook'):
            d = ole.openstream('Workbook')
            return pd.read_excel(d, engine='xlrd', dtype=dtype_map, converters=converters_map)
    except Exception as e:
        raise e

def authenticate():
    creds = None

    if os.path.exists(config['TOKEN_FILE']):
        creds = Credentials.from_authorized_user_file(config['TOKEN_FILE'], [config['SCOPES']])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config['CREDENTIALS_FILE'], [config['SCOPES']]
            )
            creds = flow.run_local_server(port=0)

        with open(config['TOKEN_FILE'], "w") as token:
            token.write(creds.to_json())

    return creds

def extract_file_id(google_sheet_url: str) -> str:
    """
    Extracts the file ID from a Google Sheets URL
    """
    return google_sheet_url.split("/d/")[1].split("/")[0]

def download_xlsx(file_id: str, creds) -> bytes:
    service = build("drive", "v3", credentials=creds)

    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()

    downloader = MediaIoBaseDownload(fh, request)
    done = False

    while not done:
        _, done = downloader.next_chunk()

    fh.seek(0)
    return fh.read()


def fetch_spreadsheet(google_sheet_link):
    creds = authenticate()
    file_id = extract_file_id(google_sheet_link)

    xlsx_data = download_xlsx(file_id, creds)
    return xlsx_data

# Save configured spreadsheets locally for testing
# purposes
def save_test_spreadsheets():
    xlsx = fetch_spreadsheet(config['pre_raft_sheet_link'])
    df = pd.read_excel(io.BytesIO(xlsx))
    with pd.ExcelWriter("test/test_files/temp_preraft.xlsx") as writer:
        df.to_excel(writer)
    
    xlsx = fetch_spreadsheet(config['post_raft_sheet_link'])
    df = pd.read_excel(io.BytesIO(xlsx))
    with pd.ExcelWriter("test/test_files/temp_postraft.xlsx") as writer:
        df.to_excel(writer)


    print ("Done saving test spreadsheets")

def load_test_spreadsheets():
    global preraft_df
    preraft_df = load_raft_spreadsheet("test/test_files/temp_preraft.xlsx")
    global postraft_df
    postraft_df = load_raft_spreadsheet("test/test_files/temp_postraft.xlsx")


def load_spreadsheet_to_df(google_sheet_link, creds, info=''):
    file_id = extract_file_id(google_sheet_link)
    xlsx_data = download_xlsx(file_id, creds)
    return load_raft_spreadsheet(io.BytesIO(xlsx_data), info=info)

def  pull_raft_spreadsheets():
    creds = authenticate()
    # this is global variable access is clumsy. Python rustiness showing through!
    try:
        global preraft_df
        preraft_df = load_spreadsheet_to_df(config['pre_raft_sheet_link'], creds, info="preraft file")
    except Exception as e:
        logging.exception(e)
        logging.critical('Unable to read pre-raft file from drive. Recommend fallback to local CSV')
        sys.exit(1)
    
    try:
        global postraft_df
        postraft_df = load_spreadsheet_to_df(config['post_raft_sheet_link'], creds, info="preraft file")
    except Exception as e:
        logging.exception(e)
        logging.critical('Unable to read post-raft file from drive. Recommend fallback to local CSV')
        sys.exit(1)


def load_dfs(is_test):
    if is_test:
        load_test_spreadsheets()
    else:
        pull_raft_spreadsheets()


