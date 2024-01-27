import pandas as pd
import time
from sqlalchemy import create_engine
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f'wget {url} -O {csv_name}')
 
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    #Create small df
    df_s = pd.read_csv(csv_name, iterator = True, chunksize = 100000)
    df = next(df_s)

    df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
    df.head(0).to_sql(name = table_name, con = engine, if_exists = 'replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    #loop to download sql
    while True:
        try:
            t_start = time.time()
            df = next(df_s)
            df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
            df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
            df.to_sql(name = table_name, con = engine, if_exists = 'append')
            t_finish = time.time()
            print(f'Another chunk added in time: {t_finish - t_start}')
        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break    

   # df2 = pd.read_csv('../data/taxi+_zone_lookup.csv') 

   # df2.head(0).to_sql(name = 'zones', con = engine, if_exists = 'replace')
   # df2.to_sql(name = 'zones', con = engine, if_exists = 'append')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Ingest csv data to postgres')

    parser.add_argument('--user', help = 'user name for postgres')
    parser.add_argument('--password', help = 'password for postgres')
    parser.add_argument('--host', help = 'host for postgres')
    parser.add_argument('--port', help = 'port for postgres')
    parser.add_argument('--db', help = 'database for postgres')
    parser.add_argument('--table_name', help = 'table_name for postgres')
    parser.add_argument('--url', help = 'url of csv file')

    args = parser.parse_args()

    main(args)

#URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"
    # docker run taxi_ingest:v001 --user=root --password=root --host=pg-database --port=5432 --db=ny_taxi --table_name=green_taxi_data --url=${URL}