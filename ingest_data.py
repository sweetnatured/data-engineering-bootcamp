import argparse
import os

import pandas as pd


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")

    df = pd.read_csv(csv_name, nrows=100)

    pd.io.sql.get_schema(df, 'green_taxi_data')

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)

    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    pd.io.sql.get_schema(df, 'green_taxi_data')

    from sqlalchemy import create_engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    engine.connect()

    pd.io.sql.get_schema(df, 'green_taxi_data', con=engine)


    df.to_sql(table_name, con=engine, if_exists='replace')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)

