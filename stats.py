def num_of_games(df, df2):
    num_of_games = df.groupby(["Team", "game_date"]).size().reset_index(name="Count")
    unique_games = num_of_games["game_date"].unique()
    avg_faceoff_wins = df2 / len(unique_games)
    formatted_avg_faceoff_wins = f"{avg_faceoff_wins:.2f}"
    return formatted_avg_faceoff_wins


def faceoff_stats(df, selected_gametype, selected_team):
    # Faceoff Data
    # Faceoff Stats
    faceoff_df = df[(df["Event"].str.contains("Faceoff")) & (df["game_type"] == selected_gametype)]
    faceoff_counts = faceoff_df.groupby(["Team"]).size().reset_index(name="Count")
    faceoff_row = faceoff_counts.loc[faceoff_counts['Team'] == selected_team, 'Count']
    #team_faceoff_counts = int(faceoff_row.iloc[0])
    if faceoff_row.empty:
        team_faceoff_counts = 0
    else:
        team_faceoff_counts = int(faceoff_row.iloc[0])

    # Number of Games 
    return num_of_games(faceoff_df, team_faceoff_counts)

    #return avg_faceoff_wins

def shots_stats(df, selected_gametype, selected_team):
    # Shot Data
    shot_df = df[(df["Event"].str.contains("Shot")) & (df["game_type"] == selected_gametype)]
    shot_counts = shot_df.groupby(["Team"]).size().reset_index(name="Count")
    shot_row = shot_counts.loc[shot_counts['Team'] == selected_team, 'Count']
    #team_shot_counts = int(shot_row.iloc[0])
    if shot_row.empty:
        team_shot_counts = 0
    else:
        team_shot_counts = int(shot_row.iloc[0])
    #return team_shot_counts
    # Number of Games 
    return num_of_games(shot_df, team_shot_counts)

def goal_data(df, selected_gametype, selected_team):
    # Goals Data
    goals_df = df[(df["Event"].str.contains("Goal")) & (df["game_type"] == selected_gametype)]
    goal_counts = goals_df.groupby(["Team"]).size().reset_index(name="Count")
    goal_row = goal_counts.loc[goal_counts['Team'] == selected_team, 'Count']
    #team_goal_counts = int(goal_row.iloc[0])
    #return team_goal_counts
    if goal_row.empty:
        team_goal_counts = 0
    else:
        team_goal_counts = int(goal_row.iloc[0])

    # Number of Games 
    return num_of_games(goals_df, team_goal_counts)