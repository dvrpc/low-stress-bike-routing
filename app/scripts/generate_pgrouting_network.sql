create table lts_ways as (
    select gid as id,
           fromnodeno::int as source,
           tonodeno::int as target,
           linklts,
           st_length(geom) * 3.28084 as len_feet,
           length * (1 + linklts + slopefac) as cost,
           10000000000000000000 as reverse_cost,
           st_transform(geom, 4326) as geom
     from
        existing_lts
     where
        geom is not null 
)