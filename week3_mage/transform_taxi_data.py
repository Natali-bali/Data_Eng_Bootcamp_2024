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
    data = data[data["passenger_count"]>0]
    data = data[data["trip_distance"]>0]
    data["lpep_pickup_date"] = data["lpep_pickup_datetime"].dt.date
    data = data.rename(columns={"VendorID": "vendor_id", "RatecodeID": "rate_code_id",\
    "PULocationID": "pu_location_id", "DOLocationID": "do_location_id"})
    return data


@test
def test_output(output, *args) -> None:
    #assert output["vendor_id"].isnull().any() == True, 'There are rides w/o vendor id'
    assert output["passenger_count"].isin([0]).sum() == 0, 'There are rides w/o passengers'
    assert output["trip_distance"].isin([0]).sum() == 0, 'There are rides w/o trip distance'
