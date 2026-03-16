SELECT
  CAST(TRIM(_c0) AS INT) AS account_id,
  TRIM(_c1) AS account_name,
  CAST(TRIM(_c2) AS INT) AS ad_id,
  TRIM(_c3) AS area,
  TRIM(_c4) AS area_name,
  TRIM(_c5) AS area_v2,
  TRIM(_c6) AS category,
  TRIM(_c7) AS category_name,
  TRIM(_c8) AS image,
  CAST(TRIM(_c9) AS DECIMAL(10,6)) AS latitude,
  CAST(TRIM(_c10) AS DECIMAL(10,6)) AS longitude,
  TRIM(_c11) AS location,
  CAST(TRIM(_c12) AS INT) AS list_id,
  CAST(TRIM(_c13) AS BIGINT) AS list_time,
  CAST(TRIM(_c14) AS BIGINT) AS price,
  TRIM(_c15) AS region_name,
  CAST(TRIM(_c16) AS INT) AS rooms,
  CAST(TRIM(_c17) AS DECIMAL(10,2)) AS size,
  TRIM(_c18) AS street_name,
  TRIM(_c19) AS subject,
  TRIM(_c20) AS type,
  TRIM(_c21) AS ward_name
FROM (
    SELECT *,
      ROW_NUMBER() OVER (ORDER BY _c0) AS row_num
    FROM csv.`s3a://warehouse/raw_input/houses.csv`
) df
WHERE row_num > 1
AND NOT (
    _c0 IS NULL OR
    _c1 IS NULL OR
    _c2 IS NULL OR
    _c3 IS NULL OR
    _c4 IS NULL OR
    _c5 IS NULL OR
    _c6 IS NULL OR
    _c7 IS NULL OR
    _c8 IS NULL OR
    _c9 IS NULL OR
    _c10 IS NULL OR
    _c11 IS NULL OR
    _c12 IS NULL OR
    _c13 IS NULL OR
    _c14 IS NULL OR
    _c15 IS NULL OR
    _c16 IS NULL OR
    _c17 IS NULL OR
    _c18 IS NULL OR
    _c19 IS NULL OR
    _c20 IS NULL OR
    _c21 IS NULL
);
