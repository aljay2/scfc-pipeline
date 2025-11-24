import pandas as pd

df = pd.read_csv("fbref_players.csv")

def fix_encoding(s):
    try:
        return s.encode("latin1").decode("utf8")
    except:
        return s

df["player_name"] = df["player_name"].apply(fix_encoding)

df.to_csv("fbref_players_cleaned.csv", index=False)

