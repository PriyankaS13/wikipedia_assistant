drop table if exists category_max_staletime;
create table  category_max_staletime
as(
select s.cat_title, max(cast(p1.page_touched as date) - cast(p.page_touched as date)) as stale_time
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
group by s.cat_title
);