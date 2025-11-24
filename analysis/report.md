# Championship Data Pipeline – Analysis Report

## 1. Objective
The project involves building and end to end data pipeline using two public football data sources, FBref and Transfermarkt, and generate an insight summary.

For the insight task, the focus is on **identifying young, high potential, U23 attackers EFL Championship**.

---

## 2. Data Sources
### **FBref**
Fbref generally supplies detailed performance statisics taken directly from match events. This is particularly valuable in finding underlying performance of players, rather than just relying on goals and assists.

The webpage containing these stats for the 25/25 season were downloaded as a HTML page. I used Python and BeautifulSoup to extract the desired table and convert them into a clean, structured dataset. 

### **Transfermarkt**
Transfermarkt focuses more on a player's background. It provides attributes such as height, nationality, footedness, contract dates, and estimated market value. 

The site loads content dynamically, so Selenium was required to scrape it. Each Championship club has its own squad page on Transfermarkt, so I built a small scraping pipeline: 
- First collect team links, 
- Then visit each squad page and extract player rows,
- Finally combine them into a single dataset.

These two sources complement each other well, FBref gives player performance and Transfermarkt gives player context. 

## 3. Data Cleaning

The datasets were cleaned and standardised so they could be used for analysis. 

The main cleaning and transformation steps included:

- Standardising column names
- Converted market value strings such as “€3.5m” or “€250k” into numeric euro values  
- Converted player height from strings like “1,85 m” into decimal metre values  
- Extracted the player’s date of birth from the combined “DOB/Age” field  
- Cleaned nationality strings to remove inconsistent spacing  
- Parsed joined dates into real datetime objects  


## 4. Cloud Ingestion
Both cleaned CSVs were saved to a Google Cloud Storage Bucket, which allowed us to load data into Google BigQuery for analysis. With GCP, the process of uploading the files and turning them into database tables was seamless, with no need to manage servers or clusters..

I made the following two tables

- `championship_data.fbref_players`
- `championship_data.transfermarkt_players`



## 4. Analysis

The analysis I chose to do was a scouting report, to identify **undervalued U23 forwards in the 2024/25 EFL Championship**. This would be faciliated both from the underlying metrics in fbref and the player metadata in transfermarkt. 

The main query used is as follows

```
-- Step 1: shortlist young forwards from FBref
WITH fb AS (
  SELECT
    player_name,
    Squad,
    Age,
    position_1,
    nineties,
    non_penalty_goals,
    expected_non_pen_goals,
    expected_assists,
    ROUND(non_penalty_goals / nineties, 2) AS npg_per90,
    ROUND(expected_non_pen_goals / nineties, 2) AS npxg_per90,
    ROUND(expected_assists / nineties, 2) AS xa_per90,
    ROUND((expected_non_pen_goals + expected_assists) / nineties, 2) AS npxgc_per90,
    ROUND(progressive_passes_received / nineties, 2) AS prg_rec_per90,
    LOWER(REGEXP_REPLACE(player_name, r'[^a-z0-9]+', '')) AS name_clean
  FROM `swansea-city-479021.championship_data.fbref_players`
  WHERE Age < 23
    AND nineties BETWEEN 5 AND 19
),

-- Step 2: transfermarkt details (cleaned)
tm AS (
  SELECT
    player_name AS tm_player_name,
    market_value_eur,
    height_m,
    foot,
    joined_date,
    signed_from,
    LOWER(REGEXP_REPLACE(player_name, r'[^a-z0-9]+', '')) AS name_clean
  FROM `swansea-city-479021.championship_data.transfermarkt_players`
)

-- Step 3: final scouting table (name-only join)
SELECT
  fb.player_name,
  fb.Squad,
  fb.Age,
  fb.position_1,
  fb.nineties,
  fb.non_penalty_goals,
  fb.expected_non_pen_goals,
  fb.expected_assists,
  fb.npg_per90,
  fb.npxg_per90,
  fb.xa_per90,
  fb.npxgc_per90,
  fb.prg_rec_per90,
  tm.market_value_eur,
  tm.height_m,
  tm.foot,
  tm.joined_date,
  tm.signed_from
FROM fb
LEFT JOIN tm
USING (name_clean)
ORDER BY npxgc_per90 DESC;

```

Initally I fetched important attacking metrics from the fbref table but crucially I filtered on age and nineties.
This allowed myself to find young players who were not established starters at their respective clubs. 

To incorporate market value, height, and player background, the cleaned FBref dataset was left joined to the Transfermarkt table using a standardised player-name key. 

Once both datasets were combined, I assessed players across several key expected metrics. These metrics together highlight forwards who consistently find good shooting locations, create chances, or receive the ball in advanced positions.

From this ranked list, I selected five players who stood out across multiple categories for inclusion in the final scouting report. These players represent the strongest blend of underlying performance and potential value in the U23 forward group.

