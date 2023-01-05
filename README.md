# Databases Project:  MakeLoveNotAccidents

| Version | Author                   | Status | Date |
| ------- | --------------------------| ------ | ----- |
|  0.2    |  Edi Zeqiri, Ugur Turhal | Ready for Analysis | 04.12.2022 |

This Project is an analysis of vehicle accidents in correlation with the speed measurements in Basel. The data are 
stored in a integrated MySQL Database and evaluated graphically in Python.

To pump the CSV in Database use the dir:
___

### Python CSV pumper

Python CSV pumper. This directory is used to pump the CSVs into a database. With the MySQL-Connector API.
___

### Integrate with SQL

The second one after Pumping the CSVs in the database please use the Intergration directory. These queries are used for
integration.
___

### Python Cleaner and CSV pumper

The Python Streetnumber directory is used to clean the first Data set.

- The first script is: ```coord_to_streetname.py``` this is used for convert coordinates to street names. And clean the
  output ```Total.csv``` up.
- The script ```Streetname_alter.sql``` is used to do make an primary key id and two entities (Hausnummer &
  Strassennummer).
- The script ```streetname_pumper.py```. Pumps the cleaned CSV in the Databases to the entity Strassenname.
- Cleaning housenumbers provides data loss. They are housenumbers missing. We have to keep them safe (providing
  dataloss). This is done by: ```save_numbers_in_streetname.py```. Output file is a csv.
- The last script that we use is the ```numberof_streetname_pumper.py``` this pumps the safed numbers to the Hausnummer
  entitiy in the Database.

### Sources:

- https://data.bs.ch/explore/dataset/100120/table/?sort=accident_date

- https://data.bs.ch/explore/dataset/100097/table/?disjunctive.geschwindigkeit&disjunctive.zone&disjunctive.ort&disjunctive.v50&disjunctive.v85&disjunctive.strasse&disjunctive.fzg&sort=timestamp

- https://data.bs.ch/explore/dataset/100200/table/?disjunctive.geschwindigkeit&disjunctive.zone&disjunctive.ort&disjunctive.v50&disjunctive.v85&disjunctive.strasse&disjunctive.fzg&sort=timestamp
