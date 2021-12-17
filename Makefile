# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif


all:
	@echo low-stress-bike-routing
	@echo -----------------------


prep-database:
	psql ${DATABASE_URL} -c 'CREATE EXTENSION IF NOT EXISTS postgis;'
	psql ${DATABASE_URL} -c 'CREATE EXTENSION IF NOT EXISTS pgrouting;'


import-data-from-dvrpc-portal-to-postgres: prep-database
	wget -O existing_lts.geojson https://opendata.arcgis.com/datasets/553b8f833da94bec99e64a28be12f34d_0.geojson
	ogr2ogr -f "ESRI Shapefile" existing_lts.shp existing_lts.geojson
	shp2pgsql -I -s 4326 existing_lts.shp existing_lts | psql ${DATABASE_URL}

