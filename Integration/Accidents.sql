create table Accidents
(
    accident_id int  not null,
    event_id    int  not null,
    description text not null,
    category    text not null,
    pedestrian  int  not null,
    bicycle     int  not null,
    motorcycle  int  not null,
    street_type text not null,
    hour        int  not null,

    primary key (accident_id),
    foreign key (event_id) references Integrated.Events (event_id)
);

create table Accidents_Junk
(
    accident_id int  not null,
    geopoint    text not null,
    geoshape    text not null,
    indicator   text not null,
    east_coord  int  not null,
    north_coord int  not null,
    Kanton      text not null,
    Gemeinde    text not null,

    primary key (accident_id),
    foreign key (accident_id) references Integrated.Accidents (accident_id)
);

insert into Accidents (accident_id, event_id, description, category, pedestrian, bicycle, motorcycle, street_type, hour)
select id, event_id, `Beschreibung zum Unfalltyp (en)`, `Beschreibung der Unfallschwerekategorie (en)`,
        `Unfall mit Fussgängerbeteiligung`, `Unfall mit Fahrradbeteiligung`, `Unfall mit Motorradbeteiligung`,
        `Beschreibung der Strassenart (en)`, Unfallstunde
from Project.Strassenverkehrsunfälle s,
     Integrated.Events e,
     Integrated.Locations l
where e.date = s.Unfalldatum
  and e.location_id = l.location_id
  and l.Street = s.Strassenname
  and l.Housenumber = s.Hausnummer;

insert into Accidents_Junk (accident_id, geopoint, geoshape, indicator, east_coord, north_coord, Kanton, Gemeinde)
select id, `Geo Point`, `Geo Shape`, `Eindeutiger Identifikator des Unfalls`, `Unfallort Ost-Koordinaten`,
        `Unfallort Nord-Koordinaten`, Kanton, Gemeindenummer
from Project.Strassenverkehrsunfälle