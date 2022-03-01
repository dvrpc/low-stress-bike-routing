# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif


all:
	@echo low-stress-bike-routing
	@echo -----------------------


prep-local-db:
	psql ${LOCAL_DATABASE_URL} -c 'CREATE EXTENSION IF NOT EXISTS postgis;'
	shp2pgsql -I -s 26918 ${SHP_PATH} existing_lts | psql ${LOCAL_DATABASE_URL}

prep-remote-db:
	psql ${REMOTE_DATABASE_URL} -c 'CREATE EXTENSION IF NOT EXISTS postgis;'
	pg_dump --no-owner --no-acl ${LOCAL_DATABASE_URL} | psql ${REMOTE_DATABASE_URL}
	psql ${REMOTE_DATABASE_URL} -c 'CREATE EXTENSION IF NOT EXISTS pgrouting;'

create-secondary-tables:
	psql ${REMOTE_DATABASE_URL} -f ./app/scripts/generate_pgrouting_network.sql
	psql ${REMOTE_DATABASE_URL} -f ./app/scripts/generate_pgrouting_network_heavyhanded.sql
	psql ${REMOTE_DATABASE_URL} -f ./app/scripts/generate_network_nodes.sql
