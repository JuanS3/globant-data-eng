-------------------------------------------------------------------------------------
-- Point 1
-------------------------------------------------------------------------------------
-- Number of employees hired for each job and department in 2021 divided by quarter.
-- The table must be ordered alphabetically by department and job.
-------------------------------------------------------------------------------------
with hired_by_qtr as (
    select
        d.department,
        j.job,
        extract('quarter' from e.hire_datetime) qtr,
        count(1) hired
    from
        departments d
        inner join employees e on e.department_id = d.id
        inner join jobs j on j.id = e.job_id
    where
        extract('year' from e.hire_datetime) = 2021
    group by
        d.department,
        j.job,
        extract('quarter' from e.hire_datetime)
)

select
    department,
    job,
    sum(case when qtr = 1 then hired else 0 end) q1,
    sum(case when qtr = 2 then hired else 0 end) q2,
    sum(case when qtr = 3 then hired else 0 end) q3,
    sum(case when qtr = 4 then hired else 0 end) q4
from
    hired_by_qtr
group by
    department,
    job
order by
    department,
    job;

-------------------------------------------------------------------------------------
-- Point 2
-------------------------------------------------------------------------------------
-- List of ids, name and number of employees hired of each department
-- that hired more employees than the mean of employees hired in 2021
-- for all the departments, ordered by the number of employees hired (descending).
-------------------------------------------------------------------------------------
with hired_by_dpt as (
    select
        d.id,
        d.department,
        count(1) hired,
        avg(count(1)) over() mean
    from
        departments d
        inner join employees e on e.department_id = d.id
    where
        extract('year' from e.hire_datetime) = 2021
    group by
        d.id,
        d.department
)

select
    id,
    department,
    hired
from
    hired_by_dpt
where
    hired > mean
order by
    hired desc;
-------------------------------------------------------------------------------------