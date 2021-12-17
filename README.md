# low-stress-bike-routing

backend that provides low-stress bike routes for the DVRPC region

## Requirements

The following command line tools are needed: `make`, `psql`, `wget`, `ogr2ogr`, `shp2pgsql`

## Environment

Create a `.env` file that defines the following variables:

```
LOCAL_DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
REMOTE_DATABASE_URL=postgresql://user:pass@hostname:port/dbname
SHP_PATH=/path/to/existing_conditions_lts.shp
```

## Commands

### Set up database

Before running any code, make sure that the databases defined in `LOCAL_DATABASE_URL` and `REMOTE_DATABASE_URL` exist.

Writing directly from shapefile to remote postgres instance will take at least 2.5 hours to run. To save time, import the spatial data to a local database, and then pipe that database to the cloud.

```
make prep-local-db
make prep-remote-db
```

Once the raw data exists in the cloud database, you'll need to run another command to create necessary tables for pgrouting:

```
make create-secondary-tables
```
