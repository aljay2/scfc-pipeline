SELECT
  player_name,
  Squad,
  position_1,
  nineties,
  expected_assists,
  ROUND(assists - expected_assists, 2) as xA_difference
FROM `swansea-city-479021.championship_data.fbref_players`
WHERE nineties >= 5
ORDER BY xA_difference ASC
LIMIT 20;
