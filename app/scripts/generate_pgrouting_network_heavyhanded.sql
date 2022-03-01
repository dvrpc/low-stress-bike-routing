create table lts_ways_heavyhanded as (
    select gid as id,
           fromnodeno::int as source,
           tonodeno::int as target,
           linklts,
           st_length(geom) * 3.28084 as len_feet,
           case
                when lts = 'LTS 1' then length
                when lts = 'LTS 2' then length * 10
                when lts = 'LTS 3' then length * 100
                when lts = 'LTS 4' then length * 1000
            end as cost,
           10000000000000000000 as reverse_cost,
           st_transform(geom, 4326) as geom
     from
        existing_lts
     where
        geom is not null 
)