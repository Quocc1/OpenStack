from dagster import repository

from .database import initialize_database
from .crawl import crawl_real_estate_website
from .end_to_end import end_to_end
from .dbt import dbt_bronze, dbt_silver, dbt_gold, dbt_all

@repository
def workspace():
  return [
    initialize_database,
    crawl_real_estate_website,
    dbt_bronze,
    dbt_silver,
    dbt_gold,
    dbt_all,
    end_to_end
  ]