import os
from dotenv import find_dotenv, load_dotenv

from typing import List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .database import postgis_query_to_geojson


load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("REMOTE_DATABASE_URL", None)
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
async def get_lowest_stress_route(start: int = Query(None), end: int = Query(None),):
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