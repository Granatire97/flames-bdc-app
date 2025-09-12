import plotly.express as px
from plotly.io import to_html

# Plot Functions Below
def zone_entry_plot1(df, selected_gametype, selected_team, selected_event="Zone Entry"):
    zone_df = df[(df["Event"].str.contains("Zone")) & (df["game_type"] == selected_gametype)]
    #zone_df["Zone"] = zone_df.apply(lambda x: rink_area(x["X Coordinate"]), axis = 1)
    team_zone_df = zone_df[zone_df["Team"]==selected_team]
    team_counts_per_period_df = team_zone_df.groupby(["game_date","Team", "Period"]).size().reset_index(name="Count")

    team_counts_per_period_df["Period"] = team_counts_per_period_df["Period"].astype("category")
    fig = px.histogram(team_counts_per_period_df, x="game_date", y="Count", color="Period", barmode="group", title="Zone Entries by Period")
    fig.update_layout(height=480, autosize=True, margin=dict(l=40,r=20,t=40,b=40))

    chart_html = to_html(fig, include_plotlyjs="cdn", full_html=False)

    return chart_html

def zone_entry_plot2(df, selected_gametype, selected_team, selected_event="Zone Entry"):
    zone_df = df[(df["Event"].str.contains("Zone")) & (df["game_type"] == selected_gametype)]
    #zone_df["Zone"] = zone_df.apply(lambda x: rink_area(x["X Coordinate"]), axis = 1)
    team_zone_df = zone_df[zone_df["Team"]==selected_team]
    team_counts_per_period_df = team_zone_df.groupby(["game_date","Team", "Detail 1"]).size().reset_index(name="Count")

    fig = px.histogram(team_counts_per_period_df, x="game_date", y="Count", color="Detail 1", barmode="group", title="Zone Entries by Detail")
    fig.update_layout(height=480, autosize=True, margin=dict(l=40,r=20,t=40,b=40))

    chart_html2 = to_html(fig, include_plotlyjs="cdn", full_html=False)

    return chart_html2

def faceoff_plot1(df, selected_gametype, selected_team, selected_event="Faceoff Win"):
    faceoff_df = df[(df["Event"].str.contains("Faceoff")) & (df["game_type"] == selected_gametype)]
    #faceoff_df["Zone"] = faceoff_df.apply(lambda x: rink_area(x["X Coordinate"]), axis = 1)
    team_faceoff_df = faceoff_df[faceoff_df["Team"]==selected_team]
    team_counts_per_period_df = team_faceoff_df.groupby(["game_date","Team", "Period"]).size().reset_index(name="Count")

    team_counts_per_period_df["Period"] = team_counts_per_period_df["Period"].astype("category")
    fig = px.bar(team_counts_per_period_df, x="game_date", y="Count", color="Period", barmode="group", title="Faceoff Wins by Period")
    fig.update_layout(height=480, autosize=True, margin=dict(l=40,r=20,t=40,b=40))

    chart_html = to_html(fig, include_plotlyjs="cdn", full_html=False)

    return chart_html

def faceoff_plot2(df, selected_gametype, selected_team, selected_zone, selected_event="Faceoff Win"):
    faceoff_df = df[(df["Event"].str.contains("Faceoff")) & (df["game_type"] == selected_gametype)]
    faceoff_zone_zone_counts = faceoff_df.groupby(["game_date","Team", "Zone"]).size().reset_index(name="Count")
    team_zone = (
    (faceoff_zone_zone_counts["Team"]==selected_team) & 
    faceoff_zone_zone_counts["Zone"].str.contains(selected_zone)
)
    team_faceoff_zone_counts = faceoff_zone_zone_counts.loc[team_zone].copy()
    fig = px.bar(team_faceoff_zone_counts, x="game_date", y="Count", color="Zone", barmode="group", title="Faceoff Wins by Zone")
    fig.update_layout(height=480, autosize=True, margin=dict(l=40,r=20,t=40,b=40))

    chart_html2 = to_html(fig, include_plotlyjs="cdn", full_html=False)
    return chart_html2

def shots_plot1(df, selected_gametype, selected_team, selected_event="Shot"):
    shot_df = df[(df["Event"].str.contains("Shot")) & (df["game_type"] == selected_gametype)]

    team_shots_df = shot_df[shot_df["Team"]==selected_team]
    team_shots_counts = team_shots_df.groupby(["Team", "game_date", "Detail 2"]).size().reset_index(name="Count")
    #team_shots_counts["game_date"] = team_shots_counts["game_date"].astype("category")
    fig = px.bar(team_shots_counts, x="game_date", y="Count", color="Detail 2", barmode="group", title="Total Shots Per Game")
    fig.update_layout(height=480, autosize=True, margin=dict(l=40,r=20,t=40,b=40))

    chart_html = to_html(fig, include_plotlyjs="cdn", full_html=False)

    return chart_html

def shots_plot2(df, selected_gametype, selected_team, selected_event="Shot"):
    shot_df = df[(df["Event"].str.contains("Shot")) & (df["game_type"] == selected_gametype)]

    team_shots_df = shot_df[shot_df["Team"]==selected_team]
    team_shots_counts_detail = team_shots_df.groupby(["Team", "Detail 2"]).size().reset_index(name="Count")
    fig = px.pie(team_shots_counts_detail, values='Count', names='Detail 2', title='Shot Details')

    chart_html2 = to_html(fig, include_plotlyjs="cdn", full_html=False)
    return chart_html2