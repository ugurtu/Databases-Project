# Get all (both sets) speeding cases in 50 zones
SELECT count(*)
FROM `Geschwindigkeitsmonitoring: Einzelmmessung bis 2020` as x,
     `Geschwindigkeitsmonitoring: Einzelmmessung ab 2021` as y
WHERE x.Geschwindigkeit > 50
  and y.Geschwindigkeit > 50
  and x.Zone = 50
  and y.Zone = 50;

# Combine both sets into one
CREATE table Geschwindigkeitsmonitoring
SELECT *
from `Geschwindigkeitsmonitoring: Einzelmmessung ab 2021`
union all
select *
from `Geschwindigkeitsmonitoring: Einzelmmessung bis 2020`;

# Group by time and location
select distinct Datum, Ort, Strasse, Hausnummer, count(*) as Anzahl
from Project.Geschwindigkeitsmonitoring
group by Datum, Ort, Strasse, Hausnummer
order by Anzahl desc;