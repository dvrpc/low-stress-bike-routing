# low-stress-bike-routing

This app is a FastAPI backend that provides low-stress bike routes for the DVRPC region using `pgrouting` queries within a `PostGIS` database. It uses DVRPC's [LTS GIS data](https://dvrpc-dvrpcgis.opendata.arcgis.com/datasets/dvrpcgis::bicycle-lts-network/about) as the analysis network.

## Requirements

The following command line tools are needed: `make`, `psql`, `wget`, `ogr2ogr`, `shp2pgsql`

## Environment

Create a `.env` file that defines the following variables:

```
LOCAL_DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
REMOTE_DATABASE_URL=postgresql://user:pass@hostname:port/dbname
SHP_PATH=/path/to/existing_conditions_lts.shp
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
# URL_PREFIX=/api/lowstress/v1  # optional
```

Note: the `DATABASE_URL` variable is used by the FastAPI app, and can point to a local or cloud-hosted database. It should be your `LOCAL_` or `REMOTE_` database URL.

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

### Run the API

For local development, you'll need to create a Python environment and install dependencies.

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

You can then run the following command from within the new environment:

```bash
uvicorn app.app.main:app --reload
```

For web deployments, a `Dockerfile` is provided.

### Use the API

The following URL pattern will return the lowest-stress route between any two nodes in the network as a geojson. In this example the route starts at node ID `735340` and ends at node ID `735389`.

```
http://localhost:8000/api/lowstress/route/?start=735340&end=735389
```
