import pandas as pd
from bs4 import BeautifulSoup, Comment


def extract_fbref_standard_stats(html_path: str, output_path: str):
    """
    Extracts the Championship Standard Stats table from an FBref HTML export.
    """    
    
    # Load HTML file
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # FBref hides tables inside HTML comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    comment_html = "\n".join(comments)

    combined_html = html + "\n" + comment_html

    # Extract all tables in the HTML
    tables = pd.read_html(combined_html)

    # Championship Standard Stats table is index 2
    df = tables[2].copy()

    # Save CSV
    df.to_csv(output_path, index=False)

    print(f"Saved to {output_path}")

    return df


if __name__ == "__main__":
    extract_fbref_standard_stats(
        html_path="fbref.html",
        output_path="fbref_players_raw.csv"
    )

