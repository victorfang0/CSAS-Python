
import pandas as pd
import numpy as np
import os

DATA_DIR = "/Users/victor/Desktop/CSAS/DATA/"
OUTPUT_PATH = "/Users/victor/Desktop/CSAS/analysis/modeling_data.csv"

def process_data():
    print("Loading data...")
    ends_df = pd.read_csv(os.path.join(DATA_DIR, "Ends.csv"))
    games_df = pd.read_csv(os.path.join(DATA_DIR, "Games.csv"))
    print(f"Ends rows: {len(ends_df)}")
    print(f"Games rows: {len(games_df)}")

    # Ensure ID columns are integers for merging
    for col in ['CompetitionID', 'GameID', 'TeamID']:
        # Fill NaNs with -1 before converting to int to avoid error
        if col in ends_df.columns:
            ends_df[col] = ends_df[col].fillna(-1).astype(int)
        
    for col in ['CompetitionID', 'GameID', 'TeamID1', 'TeamID2']:
        if col in games_df.columns:
            games_df[col] = games_df[col].fillna(-1).astype(int)

    # 1. Pivot Ends to have one row per End per Game
    # Currently it's likely one row per team per end
    # Let's verify structure by Groupby
    
    # We want a format: GameID, EndID, T1_ID, T2_ID, T1_Score, T2_Score
    
    # Check if TeamID is consistent with Games.csv
    # Games.csv has TeamID1, TeamID2
    
    # Merge Games info into Ends to identify matchups
    print("Processing game states...")
    
    # Create a list to store processed end states
    processed_rows = []
    
    # Group by Composite Key to handle reused GameIDs
    grouped_games = ends_df.groupby(["CompetitionID", "GameID"])
    
    for (comp_id, game_id), game_data in grouped_games:
        # Get game info using composite key
        # Games.csv also needs filtering
        game_matches = games_df[
            (games_df['GameID'] == game_id) & 
            (games_df['CompetitionID'] == comp_id)
        ]
        
        if game_matches.empty:
            continue
            
        game_info = game_matches.iloc[0]
        t1_id = game_info['TeamID1']
        t2_id = game_info['TeamID2']
        
        # Initial State
        t1_score_cum = 0
        t2_score_cum = 0
        
        # Hammer Logic:
        # In Mixed Doubles: 
        # End 1 Hammer: Defined by LSFE (0 or 1). 
        # If LSFE=0 (Team1?), LSFE=1 (Team2?) -> Need to verify mapping
        # Assumption: Games.csv LSFE column points to the team index?
        # Let's assume LSFE matches the index of the team in (TeamID1, TeamID2) logic or similar.
        # Deep Dive showed LSFE is 0 or 1.
        
        # Let's assume 0 -> Structure is Games[['TeamID1', 'TeamID2']]. 0 means TeamID1 has hammer.
        # We will verify this assumption by standard curling stats later if needed (e.g. usually winner of end gives up hammer).
        
        current_hammer_team = t1_id if game_info['LSFE'] == 0 else t2_id
        
        # Iterate through Ends in order
        ends_in_game = game_data.sort_values("EndID")
        unique_ends = ends_in_game['EndID'].unique()
        
        for end_num in sorted(unique_ends):
            end_frame = ends_in_game[ends_in_game['EndID'] == end_num]
            
            # Extract scores
            # Expecting 2 rows usually, one for each team
            t1_record = end_frame[end_frame['TeamID'] == t1_id]
            t2_record = end_frame[end_frame['TeamID'] == t2_id]
            
            t1_end_score = t1_record['Result'].sum() if not t1_record.empty else 0
            t2_end_score = t2_record['Result'].sum() if not t2_record.empty else 0
            
            # PowerPlay usage
            # Check if PP was used by the team WITH HAMMER
            # The PP column: Does it indicate WHO used it? Or just that it was used?
            # It has values 1.0, 2.0.
            # Likely correlates to the team.
            # Let's assume if 'PowerPlay' is not NaN in a row, that Team used it.
            pp_used = False
            pp_team = None
            
            if not t1_record.empty and pd.notna(t1_record.iloc[0]['PowerPlay']):
                pp_used = True
                pp_team = t1_id
            elif not t2_record.empty and pd.notna(t2_record.iloc[0]['PowerPlay']):
                pp_used = True
                pp_team = t2_id
                
            # Store State BEFORE the end results (for prediction)
            row_t1 = {
                'CompetitionID': comp_id,
                'GameID': game_id,
                'EndID': end_num,
                'TeamID': t1_id,
                'OpponentID': t2_id,
                'Hammer': (current_hammer_team == t1_id),
                'ScoreDiff': t1_score_cum - t2_score_cum,
                'Pre_End_Score_Own': t1_score_cum,
                'Pre_End_Score_Opp': t2_score_cum,
                'PowerPlay_Active': (pp_used and pp_team == t1_id), # Did I use PP this end?
                'PowerPlay_Opp': (pp_used and pp_team == t2_id),
                'PointsScored': t1_end_score
            }
            
            row_t2 = {
                'CompetitionID': comp_id,
                'GameID': game_id,
                'EndID': end_num,
                'TeamID': t2_id,
                'OpponentID': t1_id,
                'Hammer': (current_hammer_team == t2_id),
                'ScoreDiff': t2_score_cum - t1_score_cum,
                'Pre_End_Score_Own': t2_score_cum,
                'Pre_End_Score_Opp': t1_score_cum,
                'PowerPlay_Active': (pp_used and pp_team == t2_id),
                'PowerPlay_Opp': (pp_used and pp_team == t1_id),
                'PointsScored': t2_end_score
            }
            
            # We add results linearly to a list, we'll label 'Won_Game' later
            processed_rows.append(row_t1)
            processed_rows.append(row_t2)
            
            # Update State for next End
            t1_score_cum += t1_end_score
            t2_score_cum += t2_end_score
            
            # Update Hammer
            # Mixed Doubles Rule: Hammer ALWAYS swaps after an end
            if current_hammer_team == t1_id:
                current_hammer_team = t2_id
            else:
                current_hammer_team = t1_id

    # Create DataFrame
    model_df = pd.DataFrame(processed_rows)
    
    # Calculate Game Results (Did they win?)
    print("Calculating final results...")
    
    # We need final scores per game
    final_scores = model_df.groupby(['GameID', 'TeamID'])['ScoreDiff'].last().reset_index() 
    # Wait, 'last' ScoreDiff is at the START of the last end recorded?
    # No, we updated scores cumulatively in loop but stored 'Pre_End'.
    # We need to look at the scores AFTER the last end.
    
    # Actually, simpler: join nicely with Games.csv 'Winner' result if available?
    # Let's check if 'Winner' in Games.csv maps to 0/1 index or TeamID
    # Deep dive showed 'Winner' column: 0, 0.
    # It might be index?
    # Let's infer winner from max score in Ends df.
    
    total_scores = ends_df.groupby(['CompetitionID', 'GameID', 'TeamID'])['Result'].sum().reset_index().rename(columns={'Result': 'FinalPoints'})
    
    # Merge FinalPoints
    model_df = model_df.merge(total_scores, on=['CompetitionID', 'GameID', 'TeamID'], how='left')
    model_df = model_df.merge(total_scores.rename(columns={'TeamID': 'OpponentID', 'FinalPoints': 'OppPoints'}), on=['CompetitionID', 'GameID', 'OpponentID'], how='left')
    
    model_df['Won_Game'] = model_df['FinalPoints'] > model_df['OppPoints']
    
    # Save
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    model_df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved processed data to {OUTPUT_PATH}")
    print(model_df.head())
    print(model_df[['Hammer', 'ScoreDiff', 'PowerPlay_Active', 'Won_Game']].describe())

if __name__ == "__main__":
    process_data()
