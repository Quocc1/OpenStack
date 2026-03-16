from pathlib import Path


CITY_CODE = 13000
START_AREA = 13096
BASE_URL = "https://gateway.chotot.com/v1/public/ad-listing?"

LIMIT = 200
MAX_ERRORS = 5

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/92.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/90.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 11; SM-G960U)",
]

OUTPUT_FILE = Path("opt/dagster/stage/houses.csv")

SELECT_COLUMNS = [
    "account_id",
    "account_name",
    "ad_id",
    "area",
    "area_name",
    "area_v2",
    "category",
    "category_name",
    "image",
    "latitude",
    "longitude",
    "location",
    "list_id",
    "list_time",
    "price",
    "region_name",
    "rooms",
    "size",
    "street_name",
    "subject",
    "type",
    "ward_name",
]

BUCKET_NAME = "warehouse"
RAW_INPUT_KEY = "raw_input/houses.csv"