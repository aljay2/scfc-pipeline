from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
import os
from tmarket_scraper_links import get_driver

def extract_player_and_position(td):
    """
    Extract player name + position cell from squad table.
    """
    name_cell = td.find("td", class_="hauptlink")
    if not name_cell:
        return None, None

    name = name_cell.get_text(strip=True)
    rows = td.find_all("tr")
    position = rows[1].get_text(strip=True) if len(rows) > 1 else None

    return name, position


def extract_nation(td):
    """
    Extract nationality from flag icons.
    """
    imgs = td.find_all("img")
    return " ".join(img["alt"] for img in imgs if img.has_attr("alt"))


def extract_signed_from(td):
    """
    Extract club name from image alt tag.
    """

    img = td.find("img")
    return img["alt"] if img and img.has_attr("alt") else None



def parse_squad_html(html):
    """
    Parse a Transfermarkt squad table from HTML.
    """

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="items")

    rows = []

    for tr in table.find("tbody").find_all("tr"):
        tds = tr.find_all("td", recursive=False)
        if len(tds) < 10:
            continue

        player, position = extract_player_and_position(tds[1])
        if not player:
            continue

        row = {
            "#": tds[0].get_text(strip=True),
            "Player": player,
            "Position": position,
            "Date of birth/Age": tds[2].get_text(" ", strip=True),
            "Nat.": extract_nation(tds[3]),
            "Current club": extract_signed_from(tds[4]),
            "Height": tds[5].get_text(strip=True),
            "Foot": tds[6].get_text(strip=True),
            "Joined": tds[7].get_text(strip=True),
            "Signed from": extract_signed_from(tds[8]),
            "Market value": tds[9].get_text(strip=True),
        }

        rows.append(row)

    return pd.DataFrame(rows)



def scrape_all_squads(csv_file, output_folder="championship_players"):
    """
    Read detailed squad URLs from CSV and scrape each squad into a per-team CSV.
    """
    driver = get_driver(headless=True)

    # Create output folder if it doesn’t exist
    os.makedirs(output_folder, exist_ok=True)

    # Load detailed URLs
    detailed_urls = []
    team_names = []

    with open(csv_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            detailed_urls.append(row["detailed_team_link"])

            tn = row["team_link"].split("/")[3]  # extract slug
            tn = tn.replace("-", "_")
            team_names.append(tn)

    for team, url in zip(team_names, detailed_urls):

        driver.get(url)
        time.sleep(2)

        html = driver.page_source
        df = parse_squad_html(html)

        filename = f"{output_folder}/{team}_squad.csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")

        print(f"Saved to {filename}\n")

    driver.quit()


if __name__ == "__main__":
    scrape_all_squads("championship_team_links.csv", output_folder="championship_players")

