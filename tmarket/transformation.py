import pandas as pd
import numpy as np
import re


def parse_market_value(value):
    """
    Convert Market value strings into numeric values.
    """
    if pd.isna(value) or value == "-" or value.strip() == "":
        return np.nan

    v = value.replace("€", "").replace(",", ".").lower()

    try:
        if "m" in v:
            return float(v.replace("m", "")) * 1_000_000
        if "k" in v:
            return float(v.replace("k", "")) * 1_000
        return float(v)
    except ValueError:
        return np.nan


def parse_height(h):
    """
    Convert height from strings into floats. Eg '1,90m' to 1.90
    """
    if pd.isna(h) or h.strip() == "-":
        return np.nan

    return float(h.replace("m", "").replace(",", "."))


def extract_dob(date_string):
    """
    Extract date of birth from '10/05/2000 (25)'.
    """
    if pd.isna(date_string):
        return pd.NaT

    match = re.search(r"(\d{2}/\d{2}/\d{4})", date_string)
    if match:
        return pd.to_datetime(match.group(1), format="%d/%m/%Y")
    return pd.NaT


def clean_nat(n):
    """Clean nationality string, preserving multi-national players."""

    if pd.isna(n):
        return None
    return " ".join(n.split()).strip()

def transform_transfermarkt(input_csv, output_csv):
    """
    Transform raw Transfermarkt squad data into a clean, lightweight dataset.
    """
    df = pd.read_csv(input_csv)
    # Standardise column names
    df = df.rename(columns={
        "Player": "player_name",
        "Position": "position",
        "Date of birth/Age": "dob_age",
        "Nat.": "nationality",
        "Current club": "current_club",
        "Height": "height_raw",
        "Foot": "foot",
        "Joined": "joined_raw",
        "Signed from": "signed_from",
        "Market value": "market_value_raw",
        "Team": "team"
    })



    df["dob"] = df["dob_age"].apply(extract_dob)
    df["market_value_eur"] = df["market_value_raw"].apply(parse_market_value)
    df["height_m"] = df["height_raw"].apply(parse_height)
    df["nationality_clean"] = df["nationality"].apply(clean_nat)
    df["joined_date"] = pd.to_datetime(df["joined_raw"], errors="coerce", dayfirst=True)

    final_columns = [
        "player_name",
        "position",
        "dob",
        "nationality_clean",
        "current_club",
        "height_m",
        "foot",
        "joined_date",
        "signed_from",
        "market_value_eur",
        "team"
    ]

    df_final = df[final_columns]
    df_final.to_csv(output_csv, index=False)

    return df_final


# Run script directly
if __name__ == "__main__":
    transform_transfermarkt("championship_players_master.csv",
                            "transfermarkt_clean.csv")
