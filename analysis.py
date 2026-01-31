import pandas as pd
from config import config, get_current_raft_date, get_last_raft_date
from raft_data import get_postraft_df, get_preraft_df


# helper to format the date + name cell
def date_name_cell_val():
    d = get_current_raft_date()
    return '{} - {}/{}/{}'.format(config['initials'], d.month, d.day, d.year)

# given a data frame, returns an array of
# [Site count, Bags count, lbs]
def get_whiteboard_triplet(df):
    bag_count = df['Bags of Trash'].sum()
    return [
        len(df),
        bag_count,
        bag_count*35
    ]

# given a data frame, returns an array of
# [Site count, lbs]
def get_whiteboard_doublet(df):
    bag_count = df['Bags of Trash'].sum()
    return [
        len(df),
        bag_count*35
    ]
def get_whiteboard_bags_lbs(df):
    bag_count = df['Bags of Trash'].sum()
    return [
        bag_count,
        bag_count*35
    ]



all_sources_categories = ["Encampment Trash", "Inactive Encampment","Dumping", "Special Removal Needed", "Litter", "Stormwater Debris"]

# helper function that generates active, inactive, and all sources
# triplet for the df
def generate_df_whiteboard_vals(df, output_func):
    enc_cells = output_func(df.query("Category == 'Encampment Trash'"))
    inact_cells = output_func(df.query("Category == 'Inactive Encampment'"))
    all_source_cells = get_whiteboard_bags_lbs(df[df['Category'].isin(all_sources_categories)])
    return enc_cells + inact_cells + all_source_cells

# generate the a list of strings
# that represents the raft whiteboard row
def generate_whiteboard_output():
    df = get_postraft_df()
    # filter to San Diego (longitudes smaller than/west of the Santee longitude cutoff)
    long_cutoff = config.getfloat('longitude_cutoff_sd_all_sources')
    sd_df = df.query("Longitude < {}".format(long_cutoff))
    # filter to santee
    st_df = df.query("Longitude >= {}".format(long_cutoff))
    whiteboard_output = (generate_df_whiteboard_vals(sd_df, get_whiteboard_triplet)
                        + generate_df_whiteboard_vals(st_df, get_whiteboard_triplet)
                        + generate_df_whiteboard_vals(df, get_whiteboard_doublet)
    )
    return [date_name_cell_val()] + [str(x) for x in whiteboard_output]

# generate the a list of strings
# that represents the percent tracking row
def generate_percent_tracking():
    df = get_postraft_df()
    all_source_df = df[df['Category'].isin(all_sources_categories)]
    all_source_lbs = 35*(all_source_df['Bags of Trash'].sum())
    enc_lbs = 35*all_source_df.query("Category == '{}'".format(all_sources_categories[0]))['Bags of Trash'].sum()
    inac_lbs = 35*all_source_df.query("Category == '{}'".format(all_sources_categories[1]))['Bags of Trash'].sum()
    dump_lbs = 35*all_source_df.query("Category == '{}'".format(all_sources_categories[2]))['Bags of Trash'].sum()
    specr_lbs = 35*all_source_df.query("Category == '{}'".format(all_sources_categories[3]))['Bags of Trash'].sum()
    litt_lbs = 35*all_source_df.query("Category == '{}'".format(all_sources_categories[4]))['Bags of Trash'].sum()
    strm_lbs = 35*all_source_df.query("Category == '{}'".format(all_sources_categories[5]))['Bags of Trash'].sum()
    percent_tracking_output = [
        enc_lbs/all_source_lbs,
        inac_lbs/all_source_lbs,
        dump_lbs/all_source_lbs,
        specr_lbs/all_source_lbs,
        litt_lbs/all_source_lbs,
        strm_lbs/all_source_lbs,
        all_source_lbs,
        enc_lbs,
        inac_lbs,
        dump_lbs,
        specr_lbs,
        litt_lbs,
        strm_lbs
    ]
    return [date_name_cell_val()] + [str(x) for x in percent_tracking_output]

# team tracking constants
raft_users = ["raftintern", "RAFT1", "Raftintern", "trashcave"]
team_tracking_placeholders =["Location","Jurisdiction", "Ownership", "District", "# Vol","Event Length", "Vol Hrs", "Volunteer Names"]
							
# generate the a list of strings
# that represents the team tracking row
def generate_team_tracking():
    pre_df = get_preraft_df()
    post_df = get_postraft_df()

    # today's raft
    curr_raft_date = get_current_raft_date()
    todays_raft_df = post_df.query('uid in @raft_users and Category in @all_sources_categories and reg_datetime >= @curr_raft_date')
    todays_raft = get_whiteboard_triplet(todays_raft_df)
    # grand totals
    grand_total_trash_before_raft_df = pre_df.query('Category in @all_sources_categories')
    grand_total_trash_after_raft_df = post_df.query('Category in @all_sources_categories')
    grand_total_trash = [
        get_whiteboard_doublet(grand_total_trash_before_raft_df)[1],
        get_whiteboard_doublet(grand_total_trash_after_raft_df)[1]
    ]
    # since last raft
    last_raft_date = get_last_raft_date()
    since_last_raft_df = post_df.query('reg_datetime > @last_raft_date and  Category in @all_sources_categories')
    since_last_raft = get_whiteboard_triplet(since_last_raft_df)
    # combine output into team tracking sheet order
    team_tracking =  (['Event #', date_name_cell_val()]
             + team_tracking_placeholders
             + [str(x) for x in (todays_raft + grand_total_trash + since_last_raft)])
    return {
        'team_tracking': team_tracking,
        'team_tracking_debug_dfs': {
            'todays_raft_df': todays_raft_df,
            'grand_total_trash_before_raft_df': grand_total_trash_before_raft_df,
            'grand_total_trash_after_raft_df': grand_total_trash_after_raft_df,
            'since_last_raft_df': since_last_raft_df
        }
    }

# aggregates and returns whiteboard totals, percent tracking, and team tracking spreadsheet rows
# as comma-separated strings
def analyze():
    print("analyzing raft spreadsheet...")
    team_tracking_results = generate_team_tracking()
    return {
        "whiteboard_tracking": generate_whiteboard_output(),
        "percent_tracking": generate_percent_tracking(),
        "team_tracking": team_tracking_results['team_tracking'],
        # this is needed for team tracking splitting (not possible to automate without
        # using GIS), and also this part in the process seems to be the most capricious one
        "team_tracking_debug_dfs": team_tracking_results['team_tracking_debug_dfs']
    }
   