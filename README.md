# MLB Pitcher Post Game Report
This project is a web application built with Shiny for Python that automates the creation of post-game pitching reports using real statcast data. Users can select any MLB team, select a pitcher, choose a game date, and instantly generate:
* Summary table that shows pitch usage, velocity, spin rate, and strike percentage
* Velocity scatterplots by pitch count
* Horizontal/vertical movement scatterplots

Data is retrieved using the [Pybaseball](https://github.com/jldbc/pybaseball) and [MLB Stats API](https://github.com/toddrob99/MLB-StatsAPI) libraries. 

Link to web app using Posit Connect Cloud:
[Player Post Game Report](https://019a37da-02da-cfbc-d58f-cdb591319495.share.connect.posit.cloud/)


## Features
### Team & Pitcher Selection
* Choose any MLB team from a dropdown menu
* Automatically loads the team's current pitching staff

### Game Date Selection
* Select any date to pull Statcast pitch-by-pitch data

### Data Processing
For the selected pitcher and date, the app:
* Computes pitch counts
* Summarizes pitch types
* Calculates strike percentage per pitch
* Computers average and max velocity
* Lables opponent for home/away logic
* Formats game date into a readable format

### Visualization
* **Velocity Plot**: Pitch velocity vs. pitch number with style by pitch type
* **Movement Plot**: Horizontal vs. vertical movement

### Summary Table
Shows:
* Pitch type
* Number of pitches thrown
* Max velocity (mph)
* Average velocity (mph)
* Average spin (RPM)
* Strike percentage

## Usage
1. Select an MLB team
2. Click Submit
3. Choose a pitcher from the resulting roster
4. Select a game date
5. Click Generate Report

## File Overview
### app.py
The core Shiny app:
* Creates UI layout, sidebar, cards, and plots
* Allows the user to select team → pitcher → date
* Formats dates into readable month/day/year
* Dynamically retrieves Statcast data
* Renders:
    * Pitch data summary table
    * Velocity and movement plots
    * Opponent team name
    * Game date

Uses shiny features
* `ui.page_opts`
* `ui.sidebar`, `ui.card`
* `@reactive.event`, `@reactive.calc`
* `@render.ui`, `@render.plot`, `@render.data_frame`

### pitch_date.py
Handles all data computation and external API logic: including:
* `get_pitcher_id()` - uses Pybaseball to find MLB player IDs
* `get_pitcher_game_data()` – pulls Statcast pitch data
* `create_pitch_data_table()` – builds the main summary table (counts, spin, strike %, velocity)
* `get_opponent()` – resolves opponent abbreviation → full name
* Strike percentage calculations

### roster.py
* `get_roster()` – Fetches active roster from MLB StatsAPI
* `get_pitchers()` – Extracts pitchers from the roster listing

## Libraries
* [Shiny for Python](https://shiny.posit.co/py/)
* [Pybaseball](https://github.com/jldbc/pybaseball)
* [MLB Stats API](https://github.com/toddrob99/MLB-StatsAPI)