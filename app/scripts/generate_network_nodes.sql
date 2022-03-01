create table lts_nodes as (
    with temp_table as (
        select source as nodeid,
               st_startpoint((st_dump(geom)).geom) as geom
        from lts_ways
    )
    select nodeid, geom
    from temp_table
    group by nodeid, geom
)