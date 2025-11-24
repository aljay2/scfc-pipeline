import csv
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def get_driver(headless=False):
    """
    Launch Selenium Chrome Driver
    """
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

def convert_to_detailed_url(url):
    """
    Converts a standard team URL into the detailed squad URL.
    """
    # Replace /startseite/ with /kader/
    url = url.replace("/startseite/", "/kader/")

    # Ensure it ends with /plus/1
    if not url.endswith("/"):
        url += "/"

    if "plus/1" not in url:
        url += "plus/1"

    return url

def get_team_links(driver, url, csv_filename="team_links.csv"):
    """
    Extract all team links from a Transfermarkt league page.
    """

    print(f"Loading: {url}")
    driver.get(url)

    # Wait until team link elements appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((
            By.XPATH,
            "//td[@class='hauptlink no-border-links']/a"
        ))
    )

    link_elems = driver.find_elements(
        By.XPATH,
        "//td[@class='hauptlink no-border-links']/a"
    )

    team_links = []

    for elem in link_elems:
        href = elem.get_attribute("href")

        # Only keep valid team pages
        if not href:
            continue

        if not re.search(r"/verein/\d+", href):
            continue

        team_links.append(href)

    # Remove duplicates
    team_links = sorted(list(set(team_links)))

    print(f"Extracted {len(team_links)} unique team links")

    #write to csv
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["team_link", "detailed_team_link"])  # headers

        for link in team_links:
            detailed = convert_to_detailed_url(link)
            writer.writerow([link, detailed])

    print(f"Saved to {csv_filename}")

    return team_links


if __name__ == "__main__":
    url = "https://www.transfermarkt.co.uk/championship/startseite/wettbewerb/GB2/saison_id/2024"
    driver = get_driver(headless=False)

    try:
        links = get_team_links(driver, url, csv_filename="championship_team_links.csv")
    finally:
        driver.quit()
