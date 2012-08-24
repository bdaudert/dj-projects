<div id="content">
<textarea rows="50" cols="100" style="background-color: LightBlue;color:DarkBlue;border:1px solid Blue;font-size:20px;">
###########
Sodsum
###########
This program reads data for a list of stations and a list of
elements and provides a report on completeness of the data.  

Input:
    Coop Station Id(s)        dddddd, dddddd
    Start date                yyyymmdd
    End date                  yyyymmdd
    Element(s)                 (e.g. maxt) 

Output:
    Table one
        lists number of records found at the stations for each element
        for the given period
    Table two
        START   First date in record
        END     Last date in record
        POSBL   Possible number of observations
        PRSNT   Total number of days present in the record
        LNGPR   Largest number of consecutive observations
        MISSG   Total number of missing days
        LNGMS   Most consecutive missing observations

    Output sample

Notes:
    A day is considered present if ANY element is reported.
    NAME is the latest name of the station in the history file.
</div>
