SELECT
  id AS sale_id,
  account_id,
  ad_id,
  area,
  area_name,
  category,
  category_name,
  latitude,
  longitude,
  location,
  FROM_UNIXTIME(list_time / 1000) AS date, -- Convert Unix timestamp to standard timestamp
  price,
  region_name,
  rooms,
  size,
  type,
  EXTRACT(YEAR FROM FROM_UNIXTIME(list_time / 1000)) AS year, -- Extract year from converted timestamp
  EXTRACT(MONTH FROM FROM_UNIXTIME(list_time / 1000)) AS month, -- Extract month from converted timestamp
  CASE
    WHEN EXTRACT(MONTH FROM FROM_UNIXTIME(list_time / 1000)) IN (1, 2, 3) THEN 1
    WHEN EXTRACT(MONTH FROM FROM_UNIXTIME(list_time / 1000)) IN (4, 5, 6) THEN 2
    WHEN EXTRACT(MONTH FROM FROM_UNIXTIME(list_time / 1000)) IN (7, 8, 9) THEN 3
    ELSE 4
  END AS quarter,
  price / size AS price_per_sqm
from warehouse.bronze.bronze_raw_data