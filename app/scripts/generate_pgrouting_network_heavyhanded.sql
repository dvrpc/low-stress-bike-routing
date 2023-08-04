drop table if exists lts_ways_heavyhanded;
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
        and typeno::int not in (0, 1, 2, 3, 4, 5, 6, 10, 11, 12, 13, 14, 15, 16, 18, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99)

);