import os
import time
import random

import requests
import numpy as np
import pandas as pd
from dagster import job, op, OpExecutionContext


@op(config_schema={"output_file": str})
def crawl_real_estate_website_op(context: OpExecutionContext, dependent_job=None):
    output_file = context.op_config['output_file']
    CITY_CODE = 13000  # HCM City Code
    AREA_CODE = 13096  # 13096 to 130119 will be the area code in HCM City Code
    DEFAULT = 'https://gateway.chotot.com/v1/public/ad-listing?'
    ERROR_LIMIT = 5
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
    ]

    error = 0
    data = []
    previous = time.time()

    while True:
        page = 0
        offset = -200
        limit = 200
        context.log.info(f'Scanning area: {AREA_CODE}')

        while True:
            try:
                page += 1
                offset += 200
                url = f'{DEFAULT}region_v2{CITY_CODE}&area_v2={AREA_CODE}&cg=1000&o={offset}&page={page}&st=s,k&limit={limit}&key_param_included=true'
                headers = {'User-Agent': random.choice(user_agents)}
                r = requests.get(headers=headers, url=url)
                if 'ads' not in r.json() or len(r.json()['ads']) == 0:
                    context.log.info(f"No data available in area {AREA_CODE}")
                    break
                data.extend(r.json()['ads'])
                delta = time.time() - previous
                quantity = int(limit / delta)
                previous = time.time()
                context.log.info(
                    f'Area: {AREA_CODE} | Number of items: {page * limit} (Total: {len(data)} | Speed: {quantity} items / second)')
            except Exception as e:
                context.log.error(f'Error: {str(e)}')

            time.sleep(np.random.choice([x / 10 for x in range(3, 12)]))

        if page == 1:
            error += 1
        else:
            context.log.info(f'Finish scanning area {AREA_CODE}')

        if error > ERROR_LIMIT:
            break
        AREA_CODE += 1

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Select only the specified fields
    select_list = ['account_id', 'account_name', 'ad_id', 'area', 'area_name', 'area_v2',
                   'category', 'category_name', 'image', 'latitude', 'longitude',
                   'location', 'list_id', 'list_time', 'price', 'region_name', 'rooms',
                   'size', 'street_name', 'subject', 'type', 'ward_name']
    df = df[select_list]

    null_values = df.isnull().sum()

    context.log.info("Null values in each column:")
    context.log.info(null_values)

    # Check for null values in each column
    df = df.dropna()

    # Len of data
    context.log.info(f'Len of data: {len(df)}')

    if os.path.exists(output_file):
        os.remove(output_file)

    # Save DataFrame to CSV
    df.to_csv(output_file, mode='a', index=True, header=True, encoding='utf-8-sig')


@job()
def crawl_real_estate_website():
    crawl_real_estate_website_op()
