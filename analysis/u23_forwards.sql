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
    AND LOWER(position_1) LIKE '%fw%'
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