#HOME WORK
Question 1: What is count of records for the 2022 Green Taxi Data??

65,623,481
**840,402
1,936,423
253,647

--Create external table
CREATE OR REPLACE EXTERNAL TABLE ny_taxi.ext_green_taxi_2022
OPTIONS ( format = 'parquet',
          uris  =  ['gs://ny-taxi-zoomcamp-411215-mage-bucket/nyc_taxi_data.parquet']);

--Create materialized table
CREATE OR REPLACE TABLE ny_taxi.mat_green_taxi_2022
AS ( SELECT * FROM ny_taxi.ext_green_taxi_2022 );

--Count rows
SELECT count(1) FROM `ny_taxi.ext_green_taxi_2022`;

--Count rows
SELECT count(1) FROM `ny_taxi.mat_green_taxi_2022`;


Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

***0 MB for the External Table and 6.41MB for the Materialized Table
18.82 MB for the External Table and 47.60 MB for the Materialized Table
0 MB for the External Table and 0MB for the Materialized Table
2.14 MB for the External Table and 0MB for the Materialized Table

--Count the distinct number of PULocationIDs external table
SELECT count(DISTINCT pu_location_id) FROM `ny_taxi.ext_green_taxi_2022`;

--Count the distinct number of material table
SELECT count(DISTINCT pu_location_id) FROM `ny_taxi.mat_green_taxi_2022`;

Question 3:
How many records have a fare_amount of 0?

12,488
128,219
112
***1,622

--Count records with 0 fare
SELECT count(1) FROM `ny_taxi.ext_green_taxi_2022`
WHERE fare_amount = 0;


Question 4:
What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)

Cluster on lpep_pickup_datetime Partition by PUlocationID
***Partition by lpep_pickup_datetime Cluster on PUlocationID
Partition by lpep_pickup_datetime and Partition by PUlocationID
Cluster on by lpep_pickup_datetime and Cluster on PUlocationID

--Query to check
SELECT * FROM `ny_taxi.mat_green_taxi_2022`
WHERE lpep_pickup_date = '2022-01-01'
ORDER BY pu_location_id;
--126 Mb

--Cluster on lpep_pickup_datetime Partition by PUlocationID
--CREATE OR REPLACE TABLE ny_taxi.part_locId_clast_pickup 
--PARTITION BY
--pu_location_id AS
--SELECT * FROM `ny_taxi.ext_green_taxi_2022`;
--Patition is possible on time or array only one column

--Partition by lpep_pickup_datetime Cluster on PUlocationID
CREATE OR REPLACE TABLE ny_taxi.part_pickup_clast_locId 
PARTITION BY lpep_pickup_date 
CLUSTER BY pu_location_id
AS SELECT * FROM `ny_taxi.ext_green_taxi_2022`;
--Query to check
SELECT * FROM `ny_taxi.part_pickup_clast_locId`
WHERE lpep_pickup_date = '2022-01-01'
ORDER BY pu_location_id;
--194 KB

--Partition by lpep_pickup_datetime and Partition by PUlocationID
--CREATE OR REPLACE TABLE ny_taxi.part_locId_clast_pickup 
--PARTITION BY lpep_pickup_date 
--AS SELECT * FROM `ny_taxi.ext_green_taxi_2022`;
--Partition only possible on one column

--Cluster on by lpep_pickup_datetime and Cluster on PUlocationID--
CREATE OR REPLACE TABLE ny_taxi.clust_pickuo_clust_locId 
CLUSTER BY
lpep_pickup_date, pu_location_id AS
SELECT * FROM `ny_taxi.ext_green_taxi_2022`;
--Query to check
SELECT * FROM `ny_taxi.clust_pickuo_clust_locId`
WHERE lpep_pickup_date = '2022-01-01'
ORDER BY pu_location_id;
--438KB

Question 5:
Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values?

Choose the answer which most closely matches.

22.82 MB for non-partitioned table and 647.87 MB for the partitioned table
***12.82 MB for non-partitioned table and 1.12 MB for the partitioned table
5.63 MB for non-partitioned table and 0 MB for the partitioned table
10.31 MB for non-partitioned table and 10.31 MB for the partitioned table

--Query to check
SELECT DISTINCT pu_location_id FROM `ny_taxi.mat_green_taxi_2022`
WHERE lpep_pickup_date <= '2022-06-30' AND lpep_pickup_date >= '2022-06-01';
--12,82 Mb


--Query to check
SELECT DISTINCT pu_location_id FROM `ny_taxi.part_pickup_clast_locId`
WHERE lpep_pickup_date <= '2022-06-30' AND lpep_pickup_date >= '2022-06-01';
--1,12 Mb


Question 6:
Where is the data stored in the External Table you created?

Big Query
***GCP Bucket
Big Table
Container Registry

Question 7:
It is best practice in Big Query to always cluster your data:

True
***False






