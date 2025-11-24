import pandas as pd
import os
import glob

def combine_squad_files(folder="championship_players", output="championship_players_master.csv"):
    all_files = glob.glob(os.path.join(folder, "*_squad.csv"))

    df_list = []

    for file in all_files:
        # Extract team name from filename
        team_name = os.path.basename(file).replace("_squad.csv", "")

        # Load CSV
        df = pd.read_csv(file)

        # Add team name column
        df["Team"] = team_name

        df_list.append(df)

    # Combine all into one DataFrame
    master_df = pd.concat(df_list, ignore_index=True)
    master_df.to_csv(output, index=False, encoding="utf-8-sig")

    print(f"Saved master file as: {output}")

    return master_df

if __name__ == "__main__":
    combine_squad_files()
