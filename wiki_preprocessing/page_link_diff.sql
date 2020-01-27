drop table if exists page_link_diff;
create table page_link_diff as
(
select s.cat_title,p.page_id src_page_id,p1.page_id referred_page_id,cast(p1.page_touched as date)-cast(p.page_touched as date)as link_lag
from (select cat_title ,row_number()over(order by cat_pages desc )as rn from category)s
join categorylinks cl
on s.cat_title=cl.cl_to
join page p
on cl.cl_from=p.page_id
join pagelinks pl
on p.page_id=pl.pl_from
join page p1
on pl.pl_title=p1.page_title
where s.rn<=10
and cast(p.page_touched as date)< cast(p1.page_touched as date)
);