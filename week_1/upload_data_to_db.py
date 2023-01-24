import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from settings import BASE_DIR

load_dotenv(
    dotenv_path=f"{BASE_DIR}/docker-compose.env"
)

# Constants
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
HOST = os.getenv('POSTGRES_HOST')
PORT = os.getenv('POSTGRES_PORT')
DB = os.getenv('POSTGRES_DB')


def run():
    db_engine = create_engine(
        f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    )
    tables_config = {
        'green_taxi_trips': f"{BASE_DIR}/week_1/datasets/green_tripdata_2019-01.csv",
        'taxi_zones': f"{BASE_DIR}/week_1/datasets/taxi+_zone_lookup.csv"
    }

    for table_name, table_dataset in tables_config.items():
        print(f"Creating table {table_name} ... ")

        for chunk_df in pd.read_csv(
            filepath_or_buffer=table_dataset,
            chunksize=15000
        ):
            if table_name == 'green_taxi_trips':
                chunk_df['lpep_pickup_datetime'] = pd.to_datetime(chunk_df['lpep_pickup_datetime'])
                chunk_df['lpep_dropoff_datetime'] = pd.to_datetime(chunk_df['lpep_dropoff_datetime'])

            chunk_df.to_sql(
                name=table_name,
                if_exists="append",
                con=db_engine,
                index=False
            )

        print(f"Done!")


if __name__ == "__main__":
    run()
