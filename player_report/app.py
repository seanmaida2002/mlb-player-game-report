from shiny import reactive, render
from shiny.express import input, ui
from roster import get_roster, get_pitchers
from pitch_data import get_pitcher_id, get_pitcher_game_data, create_pitch_data_table, get_opponent
import pandas as pd
import seaborn as sns

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


ui.page_opts(title="Player Report", fillable=True)

with ui.sidebar():
    ui.input_select(
        "select_team",
        ui.tags.strong("Select a team below:"),
        {
            "Arizona Diamondbacks": "Arizona Diamondbacks",
            "Athletics": "Athletics",
            "Atlanta Braves": "Atlanta Braves",
            "Baltimore Orioles": "Baltimore Orioles",
            "Boston Red Sox": "Boston Red Sox",
            "Chicago Cubs": "Chicago Cubs",
            "Chicago White Sox": "Chicago White Sox",
            "Cincinnati Reds": "Cincinnati Reds",
            "Colorado Rockies": "Colorado Rockies",
            "Detroit Tigers": "Detroit Tigers",
            "Houston Astros": "Houston Astros",
            "Kansas City Royals": "Kansas City Royals",
            "Los Angeles Angels": "Los Angeles Angels",
            "Los Angeles Dodgers": "Los Angeles Dodgers",
            "Miami Marlins": "Miami Marlins",
            "Milwaukee Brewers": "Milwaukee Brewers",
            "Minnesota Twins": "Minnesota Twins",
            "New York Mets": "New York Mets",
            "New York Yankees": "New York Yankees",
            "Philadelphia Phillies": "Philadelphia Phillies",
            "Pittsburgh Pirates": "Pittsburgh Pirates",
            "San Diego Padres": "San Diego Padres",
            "San Francisco Giants": "San Francisco Giants",
            "Seattle Mariners": "Seattle Mariners",
            "St. Louis Cardinals": "St. Louis Cardinals",
            "Tampa Bay Rays": "Tampa Bay Rays",
            "Texas Rangers": "Texas Rangers",
            "Toronto Blue Jays": "Toronto Blue Jays",
            "Washington Nationals": "Washington Nationals"
        }
    )

    ui.tags.style("""
        #submit_team_button:hover {
            background-color: blue;  /* green background on hover */
            color: white;               /* text color on hover */
            cursor: pointer;            /* pointer cursor on hover */
            transition: background-color 0.3s ease;  /* smooth transition */
        }
    """),
    ui.input_action_button(id="submit_team_button", label="Submit")

    @render.ui
    @reactive.event(input.submit_team_button)
    def show_roster():
        selected_team = input.select_team()
        roster = get_roster(selected_team)
        pitchers = get_pitchers(roster)
        if selected_team:
            return ui.div(ui.input_select(id="select_player", label=ui.tags.strong("Select a pitcher"), choices={player: player for player in pitchers}),
                    ui.p({"style":"font-weight: bold;"}, "Choose a date:"),
                    ui.input_date("game_date", ""),
                    ui.tags.style("""
                        #get_data_button:hover {
                        background-color: blue;  /* green background on hover */
                        color: white;               /* text color on hover */
                        cursor: pointer;            /* pointer cursor on hover */
                        transition: background-color 0.3s ease;  /* smooth transition */
                        }
                    """),
                    ui.input_action_button(id="get_data_button", label="Generate Report"))


@render.ui
@reactive.event(input.get_data_button)
def header():
    date = str(input.game_date())
    player_name = input.select_player()
    parts = player_name.split()
    firstName = parts[0]
    lastName = parts[1]
    pitcher_id = get_pitcher_id(firstName=firstName, lastName=lastName)
    df = get_pitcher_game_data(pitcher_id=pitcher_id, startDate=date, endDate=date)
    if df is None or df.empty:
        return ui.div(ui.h2(player_name), ui.h3(f"{date}"))
    
    opponent_abr = df["away_team"][0]
    print(f"header: opponent_abr: {opponent_abr}")
    temp = ""
    selected_team = input.select_team()
    print(f"header: selected_team: {selected_team}")
    for key, value in team_abr.items():
        if value == opponent_abr:
            temp = key
            break
    print(f"header: temp: {temp}")
    if selected_team == temp:
         opponent_abr = df["home_team"][0]    
    print(f"header: opponent_abr: {opponent_abr}")
    opponent_name = get_opponent(opponent_abr=opponent_abr)
    return ui.div(ui.h2(player_name), ui.h3(f"{date}"), ui.h4(f"Opponent: {opponent_name}"))


with ui.layout_columns():
    @reactive.calc
    @reactive.event(input.get_data_button)
    def pitcher_data():
        date = str(input.game_date())
        player_name = input.select_player()
        parts = player_name.split()
        firstName = parts[0]
        lastName = parts[1]
        pitcher_id = get_pitcher_id(firstName=firstName, lastName=lastName)
        df = get_pitcher_game_data(pitcher_id=pitcher_id, startDate=date, endDate=date)
        return df
    
    with ui.card(full_screen=True):
        @render.data_frame
        # @reactive.event(input.get_data_button)
        def data_table():
            df = pitcher_data()
            if df is None or df.empty:
                return pd.DataFrame({"Message" : ["No data available"]})
            table = create_pitch_data_table(df=df)
            if table is None or table.empty:
                return pd.DataFrame({"Message" : ["No data available"]})
            return render.DataGrid(table)
    
    with ui.card(full_screen=True):
        @render.plot(alt="A Seaborn Plot on player's pitch movement")
        @reactive.event(input.get_data_button)
        def pitch_movement_plot():
            df = pitcher_data()
            if df is None or df.empty:
                return
            ax = sns.lineplot(data=df, x=df['pfx_x'], y=df['pfx_z'], hue=df['pitch_type'], style=df['pitch_type'])
            ax.axhline(0, color="gray", linestyle="--")
            ax.axvline(0, color="gray", linestyle="--")
            ax.set_xlabel("Horizontal Movement (ft)")
            ax.set_ylabel("Vertical Movement (ft)")
            ax.set_title("Pitch Movement")
            return ax

