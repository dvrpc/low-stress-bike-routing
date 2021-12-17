# low-stress-bike-routing

backend that provides low-stress bike routes for the DVRPC region

## Requirements

The following command line tools are needed: `make`, `psql`, `wget`, `ogr2ogr`, `shp2pgsql`

## Commands

Load data from DVRPC's ArcGIS portal to Postgres database:

```bash
make import-data-from-dvrpc-portal-to-postgres
```
