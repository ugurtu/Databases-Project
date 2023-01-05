--- For other clean up and Load in look in Python script. ---

/*
 This cleans up all fault Unfallstunde strings with 0
 */
 UPDATE `Strassenverkehrsunfälle` SET Unfallstunde = REPLACE(Unfallstunde, '?h', 0);

/*
 Update Column name from Unfallmonat since it is a Number
 */
 ALTER TABLE Strassenverkehrsunfälle
    CHANGE Unfallmonat `Unfallmonat ID` int not null;

/*
 Update Column name from Unfallmonat since it is the string
 */
ALTER TABLE Strassenverkehrsunfälle
    CHANGE `Unfallmonat.1` `Unfallmonat` text not null;

/*
 Update Column name from Unfallstunde to Unfallstunde Inter for intervall
 */
ALTER TABLE Strassenverkehrsunfälle
    CHANGE `Unfallstunde` `Unfallstunde Inter` text not null;

/*
 Update Column name from Unfallstunde.1 to Unfallstunde since it is a INT
 */
ALTER TABLE Strassenverkehrsunfälle
    CHANGE `Unfallstunde.1` `Unfallstunde` int not null;