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
    lts_table: str = Query("normal"),
):
    """
    Compute a pgrouting route solve using the request start and end node ID values

    There are two options for source table. Unless the user asks for 'heavyhanded', they will be forced to use the 'normal' table.
    """

    if lts_table == "heavyhanded":
        tablename = "lts_ways_heavyhanded"
    else:
        tablename = "lts_ways"

    query = f"""
        select
            seq,
            edge as id,
            b.len_feet,
            case 
			    when linklts >= 3 then 'true' 
				else 'false' 
			end as high_stress,
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
                    {tablename}
                ',
                {start},
                {end},
                directed => true
            ) as a
        join
            {tablename} as b
        on
            (a.edge = b.id)
        order by
            seq;
    """

    return await postgis_query_to_geojson(
        query,
        ["seq", "id", "len_feet", "geometry"],
        DATABASE_URL,
    )


async def find_nearest_node(
    lon: float,
    lat: float,
    dist_meters: float,
) -> dict:
    """
    Business logic to find the closest node to a given lon/lat
    within a specific search distance in meters.
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


@app.get(URL_PREFIX + "/nearest-node/")
async def get_nearest_node_to_lon_lat(
    lon: float = Query(None),
    lat: float = Query(None),
    dist_meters: float = Query(None),
    max_dist_meters: float = Query(804.672),
    dist_increment: float = Query(100.0),
):
    """
    Find the nearest network node to a given lon/lat, within the requested distance (in meters).
    Run this query until the nearest node is found, or the search distance exceeds the requested
    maximum distance, whichever comes first.
    """

    result = await find_nearest_node(lon, lat, dist_meters)

    # If the initial query returns nothing, continue to run the query
    # until a result is found or the search distance exceeds the maximum search distance
    while len(result["features"]) < 1 and dist_meters < max_dist_meters:
        dist_meters += dist_increment
        result = await find_nearest_node(lon, lat, dist_meters)

    return result
