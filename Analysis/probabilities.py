# 1.1 get amount of measurements
"""select count(*)
from Integrated.Measurements;"""
import pandas as pd
from Connector import Connector

# 1.2 get amount of speeding
"""select count(*)
from Integrated.Measurements
where (Zone = 50 and Speed > 55)
   or (Zone = 30 and Speed > 35)
   or (Zone = 20 and Speed > 25)
   or (Zone = 60 and Speed > 65)
   or (Zone = 80 and Speed > 85);"""

# 1.3 get percentage of speeding
"""select (select count(*)
        from Integrated.Measurements
        where (Zone = 50 and Speed > 55)
           or (Zone = 30 and Speed > 35)
           or (Zone = 20 and Speed > 25)
           or (Zone = 60 and Speed > 65)
           or (Zone = 80 and Speed > 85)) / (select count(*)
                                             from Integrated.Measurements) * 100;"""

# 2.1. get amount of accidents
"""select count(*)
from Integrated.Accidents;"""

# 2.2. get amount of accidents without parking
"""select count(*)
from Integrated.Accidents
where description != 'Accident when parking';"""

# 2.3. get percentage of accidents which might involve speeding
"""select (select count(*)
        from Integrated.Accidents
        where description != 'Accident when parking') / (select count(*) from Integrated.Accidents) * 100;"""

# 2.4. get percentage of accidents grouped by description
"""select a.description, count(*) / (select count(*) from Integrated.Accidents) * 100 as percentage
from Integrated.Accidents as a
group by description
order by percentage desc;"""

# 2.5. get amount of accidents possibly involved in speeding grouped by description
"""select a.description, count(*) as Amount
from Integrated.Accidents as a
where a.description != 'Accident when parking'
group by a.description
order by Amount desc;"""

# 3. return the street with amount of accidents in descending order
"""select a.description, l.Street, count(*) as Amount
from Integrated.Accidents as a,
     Integrated.Events as e,
     Integrated.Locations as l
where a.event_id = e.event_id
  and e.location_id = l.location_id
  and a.description != 'Accident when parking'
group by a.description, l.Street
order by Amount desc;"""

# 4. get the percentage of speeding by Quartier
"""select q.Wohnviertel,
       count(*)                                             as Anzahl,
       (count(*) * 100 / (select count(*)
                          from Integrated.Measurements as m,
                               Integrated.Events as e,
                               Integrated.Locations as l,
                               Integrated.Quartier as q
                          where m.event_id = e.event_id
                            and e.location_id = l.location_id
                            and l.Street = q.Strassenname)) as Prozent
from Integrated.Measurements as m,
     Integrated.Events as e,
     Integrated.Locations as l,
     Integrated.Quartier as q
where m.event_id = e.event_id
    and e.location_id = l.location_id
    and l.Street = q.Strassenname
    and (Zone = 50 and Speed > 55)
   or (Zone = 30 and Speed > 35)
   or (Zone = 20 and Speed > 25)
   or (Zone = 60 and Speed > 65)
   or (Zone = 80 and Speed > 85)
group by q.Wohnviertel;"""


# Get all dates and time
def month() -> pd.DataFrame:
    query = """ select e.date
    from Integrated.Measurements as m,
         Integrated.Events as e,
         Integrated.Locations as l,
         Integrated.Quartier as q
    where ((Zone = 50 and Speed > 50)
        or (Zone = 30 and Speed > 30)
        or (Zone = 20 and Speed > 20)
        or (Zone = 60 and Speed > 60)
        or (Zone = 80 and Speed > 80))
    and m.event_id = e.event_id
    and e.location_id = l.location_id;"""

    connector = Connector()

    months = connector.execute(query)

    df = pd.DataFrame(months, columns=["Month"])

    return df
