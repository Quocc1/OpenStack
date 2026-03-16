import random
import time
from typing import Dict, List, Tuple

import dagster as dg
import polars as pl
import requests
from dagster_aws.s3 import S3Resource

from .constants import (
    BASE_URL,
    BUCKET_NAME,
    CITY_CODE,
    LIMIT,
    MAX_ERRORS,
    RAW_INPUT_KEY,
    SELECT_COLUMNS,
    START_AREA,
    USER_AGENTS,
)
from .database import drop_tables


def _build_url(city_code: int, area_code: int, page: int, offset: int) -> str:
    return (
        f"{BASE_URL}region_v2={city_code}&area_v2={area_code}"
        f"&cg=1000&o={offset}&page={page}&st=s,k&limit={LIMIT}&key_param_included=true"
    )


def _fetch_ads_for_area(
    context: dg.AssetExecutionContext,
    session: requests.Session,
    city_code: int,
    area_code: int,
    previous_time: float,
) -> Tuple[List[Dict], int, float]:

    page = 0
    offset = 0
    area_data: List[Dict] = []

    context.log.info(f"Scanning area: {area_code}")

    while True:
        page += 1
        url = _build_url(city_code, area_code, page, offset)

        try:
            response = session.get(
                url,
                headers={"User-Agent": random.choice(USER_AGENTS)},
                timeout=30,
            )

            response.raise_for_status()

            payload = response.json()
            ads = payload.get("ads") or []

            if not ads:
                context.log.info(f"No more data in area {area_code}")
                break

            area_data.extend(ads)

            delta = time.time() - previous_time
            speed = int(LIMIT / delta) if delta > 0 else 0
            previous_time = time.time()

            context.log.info(
                f"Area {area_code} | Page {page} | "
                f"Fetched {len(area_data)} items | "
                f"Speed: {speed} items/sec"
            )

            offset += LIMIT

        except requests.RequestException as exc:
            context.log.error(f"Request failed for area {area_code}: {exc}")
            break

        time.sleep(random.uniform(0.3, 1.1))

    return area_data, page, previous_time


@dg.asset(deps=[drop_tables])
def crawl_real_estate_website(context: dg.AssetExecutionContext, s3: S3Resource):
    area_code = START_AREA
    error_count = 0
    previous_time = time.time()

    all_data: List[Dict] = []

    session = requests.Session()

    while error_count <= MAX_ERRORS:
        area_data, page, previous_time = _fetch_ads_for_area(
            context=context,
            session=session,
            city_code=CITY_CODE,
            area_code=area_code,
            previous_time=previous_time,
        )

        all_data.extend(area_data)

        if page == 1:
            error_count += 1
        else:
            context.log.info(f"Finished scanning area {area_code}")
            error_count = 0

        area_code += 1

    df = pl.DataFrame(all_data)

    df = df.select(SELECT_COLUMNS)

    # Normalize string columns: strip whitespace and turn empty strings into nulls
    string_columns = [
        name for name, dtype in zip(df.columns, df.dtypes) if dtype == pl.Utf8
    ]

    if string_columns:
        df = df.with_columns(
            [
                pl.col(col)
                .str.strip_chars()
                .replace("", None)
                .alias(col)
                for col in string_columns
            ]
        )

    context.log.info("Null values per column (after cleaning):")
    context.log.info(df.null_count())

    df = df.drop_nulls()

    context.log.info(f"Final dataset size: {df.height}")

    # Write to S3
    s3_client = s3.get_client()

    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=RAW_INPUT_KEY,
        Body=df.write_csv(None, include_bom=True),
    )

    context.log.info(f"Data successfully written to s3://{BUCKET_NAME}/{RAW_INPUT_KEY}")
