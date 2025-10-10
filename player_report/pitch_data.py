from pybaseball import playerid_lookup
from pybaseball import statcast_batter
from pybaseball import statcast_pitcher
import pandas as pd
import statsapi


def get_opponent(opponent_abr):
    team_codes = {"Arizona Diamondbacks": "ari", 
                  "Atlanta Braves": "atl",
                  "Baltimore Orioles": "bal",
                  "Boston Red Sox": "bos",
                  "Chicago Cubs": "chn",
                  "Chicago White Sox": "cha",
                  "Cincinnati Reds": "cin",
                  "Cleveland Guardians": "cle",
                  "Colorado Rockies": "col",
                  "Detroit Tigers": "det",
                  "Miami Marlins": "mia",
                  "Houston Astros": "hou",
                  "Kansas City Royals": "kca",
                  "Los Angeles Angels": "ana",
                  "Los Angeles Dodgers": "lan",
                  "Milwaukee Brewers": "mil",
                  "Minnesota Twins": "min",
                  "New York Mets": "nyn",
                  "New York Yankees": "nya",
                  "Athletics": "ath",
                  "Philadelphia Phillies": "phi",
                  "Pittsburgh Pirates": "pit",
                  "San Diego Padres": "sdn",
                  "San Francisco Giants": "sfn",
                  "Seattle Mariners": "sea",
                  "St. Louis Cardinals": "sln",
                  "Tampa Bay Rays": "tba",
                  "Texas Rangers": "tex",
                  "Toronto Blue Jays": "tor",
                  "Washington Nationals": "was"}
    team_abr = {"Arizona Diamondbacks": "AZ", 
                  "Atlanta Braves": "ATL",
                  "Baltimore Orioles": "BAL",
                  "Boston Red Sox": "BOS",
                  "Chicago Cubs": "CHC",
                  "Chicago White Sox": "CWS",
                  "Cincinnati Reds": "CIN",
                  "Cleveland Guardians": "CLE",
                  "Colorado Rockies": "COL",
                  "Detroit Tigers": "DET",
                  "Miami Marlins": "MIA",
                  "Houston Astros": "HOU",
                  "Kansas City Royals": "KC",
                  "Los Angeles Angels": "LAA",
                  "Los Angeles Dodgers": "LAD",
                  "Milwaukee Brewers": "MIL",
                  "Minnesota Twins": "MIN",
                  "New York Mets": "NYM",
                  "New York Yankees": "NYY",
                  "Athletics": "ATH",
                  "Philadelphia Phillies": "PHI",
                  "Pittsburgh Pirates": "PIT",
                  "San Diego Padres": "SD",
                  "San Francisco Giants": "SF",
                  "Seattle Mariners": "SEA",
                  "St. Louis Cardinals": "STL",
                  "Tampa Bay Rays": "TB",
                  "Texas Rangers": "TEX",
                  "Toronto Blue Jays": "TOR",
                  "Washington Nationals": "WSH"}
    team_code = ""
    team_name = ""
    for key,value in team_abr.items():
        if value == opponent_abr:
            team_name = key
            break
    
    for key, value in team_codes.items():
        if key == team_name:
            team_code = key
            break
    team = statsapi.lookup_team(team_code)
    team_name = team[0]['name']
    return team_name

def get_pitcher_id(firstName, lastName):
    player_id = playerid_lookup(lastName, firstName)
    pitcher_mlb_id = player_id['key_mlbam'][0]
    return pitcher_mlb_id

def get_pitcher_game_data(pitcher_id, startDate, endDate):
    statcast_pitcher_df = statcast_pitcher(startDate, endDate, pitcher_id)
    return statcast_pitcher_df

def get_strike_percentage(pitch_types_array, number_pitches, count_strikes):
    strike_percentage = {}
    for pitch in pitch_types_array:
        total = number_pitches.get(pitch, 0)
        strikes = count_strikes.get(pitch, 0)
    
        if total > 0:
            strike_percentage[pitch] = round(100 * strikes / total)
        else:
            strike_percentage[pitch] = 0
    return strike_percentage

def create_pitch_data_table(df):
    test_df = df[['pitch_type', 'pitch_name', 'description', 'release_speed', 'release_spin_rate']]
    test_df['release_speed'] = pd.to_numeric(test_df['release_speed'], errors='coerce')
    test_df['release_spin_rate'] = pd.to_numeric(test_df['release_spin_rate'], errors='coerce')
    pitch_types_array = test_df['pitch_name'].unique()
    strike_description = ['called_strike', 'swinging_strike', 'foul']
    strikes_df = test_df[test_df['description'].isin(strike_description)]
    count_strikes = strikes_df['pitch_name'].value_counts() 
    number_pitches = test_df["pitch_name"].value_counts()
    strike_percentage = get_strike_percentage(pitch_types_array, number_pitches, count_strikes)
    avg_speed = round(test_df.groupby('pitch_name')['release_speed'].mean(), 2)
    avg_spin = round(test_df.groupby('pitch_name')['release_spin_rate'].mean()).astype(int)
    max_velcoity = test_df.groupby('pitch_name')['release_speed'].max()
    new_df = pd.DataFrame(columns=['Pitch', 'Number Thrown', 'Max Velocity (MPH)', 'AVG Velocity (MPH)', 'AVG Spin (RPM)', 'Strike %'])
    new_df['Pitch'] = pitch_types_array
    new_df['Number Thrown'] = new_df['Pitch'].map(number_pitches)
    new_df['Max Velocity (MPH)'] = new_df['Pitch'].map(max_velcoity)
    new_df['AVG Velocity (MPH)'] = new_df['Pitch'].map(avg_speed)
    new_df['AVG Spin (RPM)'] = new_df['Pitch'].map(avg_spin)
    new_df['Strike %'] = new_df['Pitch'].map(strike_percentage).apply(lambda x: f"{x}%")
    return new_df.sort_values(by="Number Thrown", ascending=False)
