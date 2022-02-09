import os
from dotenv import find_dotenv, load_dotenv

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .database import postgis_query_to_geojson


load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("DATABASE_URL", None)
URL_PREFIX = os.getenv("URL_PREFIX", "")

app = FastAPI(docs_url=URL_PREFIX)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get(URL_PREFIX + "/route/")
async def get_lowest_stress_route(
    start: int = Query(None),
    end: int = Query(None),
):
    """
    Compute a pgrouting route solve using the request start and end node ID values
    """
    query = f"""
        select
            seq,
            edge as id,
            b.geom as geometry
        from
            pgr_dijkstra(
                '
                select
                    id,
                    source,
                    target,
                    cost,
                    reverse_cost
                from
                    lts_ways
                ',
                {start},
                {end},
                directed => true
            ) as a
        join
            lts_ways as b
        on
            (a.edge = b.id)
        order by
            seq;
    """

    return await postgis_query_to_geojson(
        query,
        ["seq", "id", "geometry"],
        DATABASE_URL,
    )


@app.get(URL_PREFIX + "/nearest-node/")
async def get_nearest_node_to_lon_lat(
    lon: float = Query(None),
    lat: float = Query(None),
    dist_meters: float = Query(None),
):
    """
    Find the nearest network node to a given lon/lat, within the requested distance (in meters)
    """
    query = f"""
        with user_point as (
            select ST_SetSRID(
                    ST_MakePoint({lon}, {lat}),
                    4326)::geography as geog
        )
        select
            n.nodeid,
            n.geom as geometry,
            ST_Distance(n.geom::geography, p.geog) as match_distance
        from
            lts_nodes n,
            user_point p
        where
            ST_DWithin(p.geog, n.geom::geography, {dist_meters})
        order by
            ST_Distance(n.geom::geography, p.geog) asc
        limit 1
    """

    return await postgis_query_to_geojson(
        query,
        ["nodeid", "geometry", "match_distance"],
        DATABASE_URL,
    )
