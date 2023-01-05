# How to integrate our database

After you have imported all the data, start the following sql scripts from the folder /Integrated in this specific
order:

1. `Events.sql`
2. `Measurements.sql`
3. `Accidents.sql`

**Special**: Strassenverkehrsunfälle
Since we also want to ensure that we do not have a faulty dataset
you have to run this sql script which is in the directory: Python csv pumper.

1. ```Cleaning_only_stvku.sql```

After you have done that you will need to add also the street name in the Table Strassenverkehrsunfälle:
For this use the dir: Python Streetnumber.

1. ```Streetname_alter.sql```

2. ```coord_to_streetname.py``` -> Takes ```AllCoordinates.csv``` 
Output is: ```Coordinates.csv```

3. ```streetname_pumper.py``` ->  Takes  ```Total.csv``` pumps in DB
4. ```save_numbers_in_streetname.py``` save the deleted numbers in ```Total.csv```. -> Output
   is: ```Gelöschte_Hausnummern_korrekt.csv```
5. ```numberof_streetname_pumper.py``` ->  Takes  ```Gelöschte_Hausnummern_korrekt.csv```

## Result

These scripts will integrate the `Geschwindigkeitsmonitoring` and the `Strassenverkehrsunfälle` tables into:

- `Events`
- `Measurements`
- `Accidents`
- `Locations`
