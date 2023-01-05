create table Integrated.Measurements
(
    measurement_id int  not null auto_increment,
    event_id       int  null,
    Time           text null,
    Speed          int  null,
    Zone           int  null,


    primary key (measurement_id),
    foreign key (event_id) references Integrated.Events (event_id)
);

create table Integrated.Measurements_Junk
(
    measurement_id               int   not null,
    Messung_ID                   int   null,
    Richtung_ID                  int   null,
    Messbeginn                   text  null,
    Messende                     text  null,
    Richtung                     text  null,
    Geopunkt                     text  null,
    Übertretungsquote            int   null,
    Geschwindigkeit_V50          int   null,
    Geschwindigkeit_V85          int   null,
    Kennzahlen_pro_Mess_Standort text  null,
    Fahrzeuge                    int   null,
    Fahrzeuglänge                float null,

    primary key (measurement_id),
    foreign key (measurement_id) references Integrated.Measurements (measurement_id)
);

/*
    * 1. Create a new table with the same data as the original table

 */
insert into Integrated.Measurements (measurement_id, event_id, Time, Speed, Zone)
select m.m_id, e.event_id, m.Zeit, m.Geschwindigkeit, m.Zone
from Integrated.Events as e,
     Integrated.Locations as l,
     Project.Geschwindigkeitsmonitoring as m
where e.location_id = l.location_id
  and e.date = m.Datum
  and l.location = m.Ort
  and l.street = m.Strasse
  and l.HouseNumber = m.Hausnummer;

insert into Integrated.Measurements_Junk (measurement_id, Messung_ID, Richtung_ID, Messbeginn, Messende, Richtung,
                                          Geopunkt, Übertretungsquote, Geschwindigkeit_V50, Geschwindigkeit_V85,
                                          Kennzahlen_pro_Mess_Standort, Fahrzeuge, Fahrzeuglänge)
select m_id,
       `Messung-ID`,
       `Richtung ID`,
       Messbeginn,
       Messende,
       Richtung,
       Geopunkt,
       Übertretungsquote,
       `Geschwindigkeit V50`,
       `Geschwindigkeit V85`,
       `Kennzahlen pro Mess-Standort`,
       Fahrzeuge,
       Fahrzeuglänge

from Project.Geschwindigkeitsmonitoring;




