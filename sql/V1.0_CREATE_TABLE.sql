CREATE SCHEMA if not exists reporting;

CREATE TABLE if not exists reporting.tbl_taxi(
    index bigint,
    filename text,
    vendor_id bigint,
    tpep_pickup_datetime timestamp without time zone not null,
    tpep_dropoff_datetime timestamp without time zone not null,
    pickup_year integer,
    pickup_month integer,
    pickup_day integer,
    pickup_hour integer,
    dropoff_hour integer,
    passenger_count integer,
    trip_distance double precision,
    ratecode_id integer,
    store_and_fwd_flag text,
    pu_location_id integer,
    do_location_id integer,
    payment_type integer,
    fare_amount double precision,
    extra double precision,
    mta_tax double precision,
    tip_amount double precision,
    tolls_amount double precision,
    improvement_surcharge double precision,
    total_amount double precision,
    congestion_surcharge double precision,
    taxi_color text,
    primary key(index,filename)
);

CREATE INDEX IF NOT EXISTS reporting_tbl_taxi ON reporting.tbl_taxi (pickup_year,pickup_month,pickup_day);



CREATE TABLE if not exists  reporting.tbl_status (
  id              SERIAL PRIMARY KEY,
  filename text,
  updated_datetime timestamp,
  status  TEXT NOT NULL
);