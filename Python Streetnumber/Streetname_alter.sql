-- Path: Python Streetnumber/Streetname_alter.sql

/**
  Make new attribute for Streetname
 */
ALTER TABLE Strassenverkehrsunfälle ADD `Strassenname` TEXT NOT NULL;

/**
  Make id, needed for @file streetname_pumper.py and streetnumber_pumper.py
  Since we want to update the records we need to have an id.
 */
ALTER TABLE Strassenverkehrsunfälle
    ADD `id` INT  NOT NULL AUTO_INCREMENT PRIMARY KEY AFTER `Geo Point`;

/**
  Make new attribute for Streetnumber
 */
alter table Strassenverkehrsunfälle
    add Hausnummer int not null;