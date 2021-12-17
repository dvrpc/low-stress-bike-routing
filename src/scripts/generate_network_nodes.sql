create table lts_nodes as
    (select source as nodeid,
                      st_startpoint((st_dump(geom)).geom) as geom
     from lts_ways)