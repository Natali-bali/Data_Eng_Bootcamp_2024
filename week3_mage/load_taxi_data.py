import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):

    link = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_'
    year = 2020
    months = ['10', '11', '12']
    
    taxi_dtypes = {
                "VendorID": pd.Int64Dtype(),
                "store_and_fwd_flag": str,
                "RatecodeID": pd.Int64Dtype(),
                "PULocationID": pd.Int64Dtype(),
                "DOLocationID": pd.Int64Dtype() ,
                "passenger_count": pd.Int64Dtype(),
                "trip_distance": float,
                "fare_amount": float,
                "extra": float,
                "mta_tax": float,
                "tip_amount": float,
                "tolls_amount": float,
                "ehail_fee": float,
                "improvement_surcharge": float,
                "total_amount": float,
                "payment_type": pd.Int64Dtype(),
                "trip_type":  pd.Int64Dtype(),
                "congestion_surcharge": float 
                }
    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime'] 

    return pd.concat(( \
    pd.read_csv('{}{}-{}.csv.gz'.format(link, year, month), \
     sep=',', dtype=taxi_dtypes, compression='gzip', parse_dates=parse_dates) \
    for month in months), ignore_index=True)
    
  


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

    import pandas as pd
from datetime import date
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
#Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero.
#Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
#Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id.
#Add three assertions:
#vendor_id is one of the existing values in the column (currently)
#passenger_count is greater than 0
#trip_distance is greater than 0
    print(f'Processing: number of rides with 0 passengers: {data["passenger_count"].isin([0]).sum()} removed')
    print(f'Processing: number of rides with 0 km distance: {data["trip_distance"].isin([0]).sum()} removed')
#    print(f'Processing: number of rides with 0 payment: {data["fare_amount"].isin([0]).sum()}')
    data = data[data["fare_amount"]>0]
    data = data[data["trip_distance"]>0]
    data["lpep_pickup_date"] = data["lpep_pickup_datetime"].dt.date
    data = data.rename(columns={"VendorID": "vendor_id", "RatecodeID": "rate_code_id",\
    "PULocationID": "pu_location_id", "DOLocationID": "do_location_id"})
    return data


@test
def test_output(output, *args) -> None:
    assert output["vendor_id"].isin([0]).sum() == 0, 'There are rides w/o payments'
    assert output["fare_amount"].isin([0]).sum() == 0, 'There are rides w/o payments'
    assert output["fare_amount"].isin([0]).sum() == 0, 'There are rides w/o payments'

