create table if not exists Integrated.Locations
(
    location_id int  not null auto_increment,
    Location    text not null,
    Street      text not null,
    HouseNumber text,

    primary key (location_id)
);

create table if not exists Integrated.Events
(
    event_id    int  not null auto_increment,
    date        text not null,
    location_id int  not null,

    primary key (event_id),
    foreign key (location_id) references Integrated.Locations (location_id)
);

/*
    Combine the two tables into one.
 */
create table if not exists Project.Geschwindigkeitsmonitoring
select *
from Project.`Geschwindigkeitsmonitoring: Einzelmmessung ab 2021`
union all
select *
from Project.`Geschwindigkeitsmonitoring: Einzelmmessung bis 2020`;

/*
    Insert distinct locations (Ort,Strasse,Hausnumme) into the Locations table from the original data sets
*/
insert into Integrated.Locations (Location, Street, HouseNumber)
    (select g.Ort,
            g.Strasse,
            g.Hausnummer
     from Project.Geschwindigkeitsmonitoring as g)
union
(select 'Basel', Strassenname, Hausnummer
 from Project.Strassenverkehrsunfälle);
/*
update Project.Geschwindigkeitsmonitoring set Datum = date_format(str_to_date(Datum, '%d.%m.%y'), '%Y-%m')
*/
/*
    Insert distinct combinations of events (date, location) into the Events table from the original Measurements table
*/
insert into Integrated.Events (date, location_id)
select distinct g.Datum, l.location_id
from Project.Geschwindigkeitsmonitoring as g,
     Integrated.Locations as l
where g.Ort = l.Location
  and g.Strasse = l.Street
  and g.Hausnummer = l.HouseNumber
group by Datum, l.location_id;

/*
 Insert distinct combination of events (date, location) into the Events table from the original Accidents table
 */
insert into Integrated.Events (date, location_id)
select distinct Unfalldatum, l.location_id
from Project.Strassenverkehrsunfälle as u,
     Integrated.Locations as l
where u.Strassenname = l.Street
  and u.Hausnummer = l.HouseNumber
group by Unfalldatum, l.location_id;
