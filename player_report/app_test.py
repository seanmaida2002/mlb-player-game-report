import seaborn as sns
from faicons import icon_svg

# Import data from shared.py
from shared import app_dir, df

from shiny import reactive
from shiny.express import input, render, ui

ui.page_opts(title="Player Report", fillable=True)


with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

# with ui.sidebar(title="Filter controls"):
#     ui.input_select(
#         "select",
#         "Select a team below:",
#         {
#             "Arizona Diamondbacks": "Arizona Diamondbacks",
#             "Athletics": "Athletics",
#             "Atlanta Braves": "Atlanta Braves",
#             "Baltimore Orioles": "Baltimore Orioles",
#             "Boston Red Sox": "Boston Red Sox",
#             "Chicago Cubs": "Chicago Cubs",
#             "Chicago White Sox": "Chicago White Sox",
#             "Cincinnati Reds": "Cincinnati Reds",
#             "Colorado Rockies": "Colorado Rockies",
#             "Detroit Tigers": "Detroit Tigers",
#             "Houston Astros": "Houston Astros",
#             "Kansas City Royals": "Kansas City Royals",
#             "Los Angeles Angels": "Los Angeles Angels",
#             "Los Angeles Dodgers": "Los Angeles Dodgers",
#             "Miami Marlins": "Miami Marlins",
#             "Milwaukee Brewers": "Milwaukee Brewers",
#             "Minnesota Twins": "Minnesota Twins",
#             "New York Mets": "New York Mets",
#             "New York Yankees": "New York Yankees",
#             "Philadelphia Phillies": "Philadelphia Phillies",
#             "Pittsburgh Pirates": "Pittsburgh Pirates",
#             "San Diego Padres": "San Diego Padres",
#             "San Francisco Giants": "San Francisco Giants",
#             "Seattle Mariners": "Seattle Mariners",
#             "St. Louis Cardinals": "St. Louis Cardinals",
#             "Tampa Bay Rays": "Tampa Bay Rays",
#             "Texas Rangers": "Texas Rangers",
#             "Toronto Blue Jays": "Toronto Blue Jays",
#             "Washington Nationals": "Washington Nationals"
#         }
#     )

#     ui.tags.style("""
#         #submit_team_button:hover {
#             background-color: blue;  /* green background on hover */
#             color: white;               /* text color on hover */
#             cursor: pointer;            /* pointer cursor on hover */
#             transition: background-color 0.3s ease;  /* smooth transition */
#         }
#     """),
#     ui.input_action_button(id="submit_team_button", label="Submit")

with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
