--NPxG Overperformers/Underperformers
SELECT
  player_name,
  Squad,
  position_1,
  nineties,
  non_penalty_goals,
  expected_non_pen_goals,
  ROUND(non_penalty_goals - expected_non_pen_goals, 2) AS npxg_difference,
FROM `swansea-city-479021.championship_data.fbref_players`
WHERE nineties >= 5
ORDER BY npxg_difference ASC
LIMIT 20;
