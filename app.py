from flask import Flask, render_template, jsonify, request, redirect, url_for
import pandas as pd
from pathlib import Path

from stats import faceoff_stats, shots_stats, goal_data
from charts import (
    zone_entry_plot1,
    zone_entry_plot2,
    faceoff_plot1,
    faceoff_plot2,
    shots_plot1,
    shots_plot2,
)

app = Flask(__name__)

DATA_PATH = Path("data/files/olympic_womens_dataset.csv")
df = pd.read_csv(DATA_PATH)

# Drop NCAA Teams
df = df.drop(df[df["Team"].isin(["St. Lawrence Saints", "Clarkson Golden Knights"])].index)

# Rename Teams
df["Team"] = df["Team"].replace({
    "Olympic (Women) - Canada": "Canada",
    "Olympic (Women) - Olympic Athletes from Russia": "Russia",
    "Olympic (Women) - Finland": "Finland",
    "Olympic (Women) - United States": "USA"
})

# Make Game/Date a DateTime
df['game_date'] = pd.to_datetime(df['game_date'])

# Function for Type of Game Event
def game_type(game_date):
    dt = game_date
    
    if dt.year == 2018 and dt.month == 2:
        type = "Olympic Games"
    elif dt.year == 2019 and dt.month == 2:
        type = "US vs Canada - Rivalry Games"
    else:
        type = "World Championships"
    return type

df["game_type"] = df["game_date"].apply(game_type)

# Zone Filter For Search
def rink_area(x):
    if 0 <= x < 75:
        return "Defensive Zone"
    elif 75 <= x <= 125:
        return "Neutral Zone"
    else: 
        return "Offensive Zone"
        
df["Zone"] = df.apply(lambda x: rink_area(x["X Coordinate"]), axis = 1)

# Event Filter For Search
event_filter = df[df["Event"].str.contains("Faceoff") | df["Event"].str.contains("Zone") | df["Event"].str.contains("Shot")]

# First Screen
@app.route("/")
def index():
    return render_template("index.html")

# Coaches Dashboard Screen
@app.route('/coach', methods=['POST', 'GET'])
def coach():
    game_type_list = df["game_type"].unique()
    team_names = df["Team"].unique()
    event_types = event_filter['Event'].unique()
    zone_list = df['Zone'].unique()
    
    if request.method == 'POST':
        selected_gametype   = request.form.get('gametype', '')
        selected_team   = request.form.get('team', '')
        selected_event  = request.form.get('event', '')
        selected_zone = request.form.get('zone', '')

        if selected_gametype and not selected_team and not selected_event and not selected_zone:
            return redirect(url_for('coach_gametype', selected_gametype=selected_gametype))
        if selected_gametype and selected_team and not selected_event and not selected_zone:
            return redirect(url_for('coach_gametype_team', selected_gametype=selected_gametype, selected_team=selected_team))
        if selected_gametype and selected_team and selected_event and not selected_zone:
            return redirect(url_for('coach_gametype_team_event', selected_gametype=selected_gametype, selected_team=selected_team, selected_event=selected_event))
        if selected_gametype and selected_team and selected_event and selected_zone:
            return redirect(url_for('coach_gametype_team_event_zone', selected_gametype=selected_gametype, selected_team=selected_team, selected_event=selected_event, selected_zone=selected_zone))
    
    else:
        selected_gametype = request.args.get('gametype', '')
        selected_team   = request.args.get('team', '')
        selected_event  = request.args.get('event', '')
        selected_zone = request.args.get('zone', '')

    return render_template(
        'coach.html',
        game_type_list=game_type_list,
        team_names=team_names,
        event_types=event_types,
        zone_list=zone_list,
        selected_gametype=selected_gametype,
        selected_team=selected_team,
        selected_event=selected_event,
        selected_zone=selected_zone,
    )

# Team Routing
@app.route('/coach/<selected_gametype>')
def coach_gametype(selected_gametype):
    game_type_list = df["game_type"].unique()
    team_names = df["Team"].unique()
    event_types = event_filter["Event"].unique()
    zone_list = df["Zone"].unique()

    return render_template(
        'coach.html',
        team_names=team_names,
        event_types=event_types,
        zone_list=zone_list,
        game_type_list=game_type_list,
        selected_gametype=selected_gametype
    )
@app.route('/coach/<selected_gametype>/<selected_team>')
def coach_gametype_team(selected_gametype, selected_team):
    game_type_list = df["game_type"].unique()
    team_names = df["Team"].unique()
    event_types = event_filter["Event"].unique()
    zone_list = df["Zone"].unique()

    return render_template(
        'coach.html',
        team_names=team_names,
        event_types=event_types,
        zone_list=zone_list,
        game_type_list=game_type_list,
        selected_gametype=selected_gametype,
        selected_team=selected_team,
        team_faceoff_counts=faceoff_stats(df, selected_gametype, selected_team),
        team_shot_counts=shots_stats(df, selected_gametype, selected_team),
        team_goal_counts=goal_data(df, selected_gametype, selected_team)
    )

# Event Routing
@app.route('/coach/<selected_gametype>/<selected_team>/<selected_event>')
def coach_gametype_team_event(selected_gametype,selected_team, selected_event):
    game_type_list = df["game_type"].unique()
    team_names = df["Team"].unique()
    event_types = event_filter["Event"].unique()
    zone_list = df["Zone"].unique()

    if selected_event == "Zone Entry":
        chart_label = "Zone Entries Visualizations"
        plot1 = zone_entry_plot1(df, selected_gametype, selected_team)
        plot2 = zone_entry_plot2(df, selected_gametype, selected_team)
    elif selected_event == "Faceoff Win":
        chart_label = "Faceoff Win By Period"
        plot1 = faceoff_plot1(df, selected_gametype, selected_team)
        plot2 = url_for('static', filename='img/no_visual.png')
    else:
        chart_label = "Shot Statistics"
        plot1 = shots_plot1(df, selected_gametype, selected_team)
        plot2 = shots_plot2(df, selected_gametype, selected_team)

    return render_template(
        'coach.html',
        team_names=team_names,
        event_types=event_types,
        zone_list=zone_list,
        game_type_list=game_type_list,
        selected_gametype=selected_gametype,
        selected_team=selected_team,
        selected_event=selected_event,
        chart_label=chart_label,
        team_faceoff_counts=faceoff_stats(df, selected_gametype, selected_team),
        team_shot_counts=shots_stats(df, selected_gametype, selected_team),
        team_goal_counts=goal_data(df, selected_gametype, selected_team),
        chart_html=plot1,
        chart_html2=plot2
    )

# Zone Filter For Faceoffs 
@app.route('/coach/<selected_gametype>/<selected_team>/<selected_event>/<selected_zone>')
def coach_gametype_team_event_zone(selected_gametype, selected_team, selected_event, selected_zone):
    game_type_list = df["game_type"].unique()
    team_names = df["Team"].unique()
    event_types = event_filter["Event"].unique()
    zone_list = df["Zone"].unique()

    if selected_event == "Faceoff Win":
        chart_label = "Faceoff Wins By Zone"
        plot1 = faceoff_plot2(df, selected_gametype, selected_team, selected_zone)
        plot2 = url_for('static', filename='img/no_visual.png')
    else:
        chart_label = 'No Visualizations Present'
        plot1 = url_for('static', filename='img/no_visual.png')
        plot2 = url_for('static', filename='img/no_visual.png')

    return render_template(
        'coach.html',
        team_names=team_names,
        event_types=event_types,
        zone_list=zone_list,
        game_type_list=game_type_list,
        selected_gametype=selected_gametype,
        selected_team=selected_team,
        selected_event=selected_event, 
        selected_zone=selected_zone,
        chart_label=chart_label,
        chart_html=plot1,
        chart_html2=plot2,
        team_faceoff_counts=faceoff_stats(df, selected_gametype, selected_team),
        team_shot_counts=shots_stats(df, selected_gametype, selected_team),
        team_goal_counts=goal_data(df, selected_gametype, selected_team)
    )

if __name__ == "__main__":
    app.run(debug=True)
