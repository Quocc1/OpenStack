SELECT ad_id AS sale_id,
  account_id,
  account_name,
  ad_id,
  area,
  area_name,
  area_v2,
  category,
  category_name,
  image,
  latitude,
  longitude,
  location,
  street_name,
  ward_name,
  FROM_UNIXTIME(list_time / 1000) AS date,
  price,
  region_name,
  rooms,
  size,
  type,
  EXTRACT(
    YEAR
    FROM FROM_UNIXTIME(list_time / 1000)
  ) AS year,
  EXTRACT(
    MONTH
    FROM FROM_UNIXTIME(list_time / 1000)
  ) AS month,
  CASE
    WHEN EXTRACT(
      MONTH
      FROM FROM_UNIXTIME(list_time / 1000)
    ) IN (1, 2, 3) THEN 1
    WHEN EXTRACT(
      MONTH
      FROM FROM_UNIXTIME(list_time / 1000)
    ) IN (4, 5, 6) THEN 2
    WHEN EXTRACT(
      MONTH
      FROM FROM_UNIXTIME(list_time / 1000)
    ) IN (7, 8, 9) THEN 3
    ELSE 4
  END AS quarter,
  price / NULLIF(size, 0) AS price_per_sqm
FROM bronze.bronze_raw_data
WHERE price > 0 AND size > 0
