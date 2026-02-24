# Championship Data Pipeline

This project builds a small, end-to-end **data pipeline** to collect player data for the 2024/25 EFL Championship.

## Overview
- Stored raw files in **Google Cloud Storage**
- Cleaned and transformed both datasets using Python
- Produced a short **scouting insight report** using SQL + visualisations
- Loaded cleaned data into **BigQuery**
- Scraped **FBref** and **Transfermarkt**
- Testing to see if i get alert



## Architecture
The pipeline consists of:
1. **Scrapers** that collect raw data from FBref and Transfermarkt  
2. **Transformation scripts** that clean, standardise, and reshape the data  
3. **Cloud storage** where raw and cleaned files are uploaded  
4. **BigQuery tables** that store the cleaned datasets  
5. **A report** that runs explains analysis   
6. **A final PDF report** summarising insights



## Setup Instructions

### 1. Clone the repository and activate a venv
```bash
cd scfc-pipeline
git clone https://github.com/AlJay1/scfc-pipeline.git
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```
### 2. Install requirements
```
pip install -r requirements.txt
```

### 3. Run the respective scrapers
```
python /transfermarkt/get_team_links.py
python /transfermarkt/scrape_squads.py
python /transfermarkt/combine_squad_files.py
python /transfermarkt/transform_transfermarkt.py


python /fbref/fbref_player_scrape.py.py
python /fbref/fbref_clean.py

```
### 4. Cloud ingestion

Upload fbref_players_cleaned.csv and transfermarkt_clean.csv to your GCP storage bucket and generate bigquery tables.

### 5. Insights
Run the sql files in the analysis folder on your BigQuery Tables.
