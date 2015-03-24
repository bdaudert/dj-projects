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


Sample Output:

Summary of daily observations by element. Last date considered : 20121012 

STATION        START             END       pcpn    snow    snwd    maxt    mint    obst
103732      20120101        20121012        286     271     269     280     279     262
266779      20120101        20121012        285     284     285     285     285     0

SUMMARY-OF-THE-DAY STATISTICS
          Last date considered for this listing : 20120101
          START - First date in record (YYMMDD)
          END - Last date in record (YYMMDD)
          POSBL - Possible number of observations
          PRSNT - Total number of days present in the record
          LNGPR - Largest number of consecutive observations
          MISSG - Total number of missing days
          LNGMS - Most consecutive missing observations
A day is considered present if any element is reported.
NAME is the latest name of the station in the history file.

NUMBER                    NAME         START             END      POSBL   PRSNT   LNGPR   MISSG   LNGMS
103732      GRACE                   20120101        20121012        286     286     286     0       0
266779      RENO TAHOE INTL AP      20120101        20121012        286     285     285     1       1



Notes:
    A day is considered present if ANY element is reported.
    NAME is the latest name of the station in the history file.
</div>