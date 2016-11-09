<div id="content">
<textarea rows="50" cols="100" style="background-color: LightBlue;color:DarkBlue;border:1px solid Blue;font-size:20px;">
###########
Sodpiii
###########

This program finds the extreme value of a climate element for a
1-day, 2-day, 3-day,....9-day, 10-day, 10, 15, 20, 25 and 30-day period within
a 12 month window each year.  The user specifies the
starting month of the 12-month window.
Statistics are then determined for each duration, and
values are then calculated for various recurrence
intervals, exceedance and non-exceedance probabilities.
The coefficient of variation and skewness may be determined
from the station record, or from externally supplied     
areal values, as suggested by Jim Goodridge (CA).       
(This feature temporarily suspended)
Other elements may be used: Max and min temperature,
snowfall, and snowdepth (for instance to find the warmest
3-day average maximum expected every 10 years)           
The value given is the extreme from periods that START in  
the year as defined.  The date given is the START of the
interval.

Input:
    Coop Station Id(s)      dddddd, dddddd
    Start date              yyyymm
    End date                yyyymm
    Element
    Skew type: Areal/Station
    Cv   type: Areal/Station       
    Mean type: Areal/Station
    Pct Average type: Areal/Station
    Number of days: 1-5, and individual day between 1 and 30 or all
    Value to set for subsequent data [9991]
    Value to set for missing data[9999]
    
Sample Output:

    STATION NUMBER 266779
 LOCATION :                               
 ELEMENT : PRECIP   UNITS : .01 'S INCHES 
 DURATION :  20 DAY(S).    START MONTH :   1
 AVERAGE =    2.040   ST DEV =  0.141   SKEWNESS = -0.002
 ADJUSTMENT OF 1.00 APPLIED FOR CLOCK EFFECTS
 USES OBSERVATION DAYS ONLY

   Prob of    Prob of       Return     Value in       Value in 
 Nonxceednce Exceedance Interval (yr)  Std. Dev.    Absolute units
 ----------- ---------- ------------- ------------- -----------------

 PN = 0.0001 P = 0.9999 T =    1.0001 PSD =  -3.724 VALUE =     1.51"
 PN = 0.0002 P = 0.9998 T =    1.0002 PSD =  -3.616 VALUE =     1.53"
 PN = 0.0003 P = 0.9997 T =    1.0003 PSD =  -3.509 VALUE =     1.54"
 PN = 0.0004 P = 0.9996 T =    1.0004 PSD =  -3.401 VALUE =     1.56"
 PN = 0.0005 P = 0.9995 T =    1.0005 PSD =  -3.293 VALUE =     1.57"
    
    

Notes:

</div>
