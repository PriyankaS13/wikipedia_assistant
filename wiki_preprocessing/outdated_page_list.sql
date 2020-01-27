drop table if exists outdated_page_list;
create table outdated_page_list
as
(
select distinct cast(p.cat_title as char(4000)) as category,p.src_page_id as outdated_page_id
from page_link_diff p join category_max_staletime c
on p.cat_title=c.cat_title and p.link_lag=c.stale_time
);