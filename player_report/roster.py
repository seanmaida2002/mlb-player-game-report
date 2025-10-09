import statsapi
from datetime import datetime

def get_roster(teamName):
    team = statsapi.lookup_team(teamName)
    team_id = team[0]['id']
    roster = statsapi.roster(team_id, season=datetime.now().year)
    return roster

def get_pitchers(roster):
    lines = roster.strip().split("\n")
    pitchers = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 3 and parts[1] == "P":
            name = " ".join(parts[2:])
            pitchers.append(name)
    return pitchers