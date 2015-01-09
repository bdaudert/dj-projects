<div id="content">
<textarea rows="50" cols="100" style="background-color: LightBlue;color:DarkBlue;border:1px solid Blue;font-size:20px;">
###########
Sodpad
###########
This program computes probability accumulation duration for precipitationi for each day of the year.
i.e. it computes the probability to abtain a certain amount of precip in a certain number of days.

Input:
    Coop Station Id(s)      dddddd, dddddd
    Start date              yyyy
    End date                yyyy
    
Sample Output:

PRECIPITATION-DURATION-FREQUENCY TABLES FOR STATION: 266779 RENO TAHOE INTL AP
BASED ON PERIOD 2000 TO 2011

STN=266779 MON=1 DAY=1

THRESHOLD:        01    10   15   20    25   30 ...
DURATION = 1    11.2  25.0 16.7 16.7  16.7 16.7 ...
                41.7  25.0 25.0 16.7   8.3  8.3 ...

...
...
STN=266779 MON=12 DAY=31

THRESHOLD:        01    10   15   20    25   30 ...
DURATION = 1    66.7  25.0 33.3  8.3   0.0  0.0 ...
                41.7  25.0 25.0 16.7   8.3  0.0 ...


Notes:
!!!!!!!!!!!!!
WARNING!!!!!!Since probabilities are computed for each day, the program may take a while to run, especially when multiple stations are selected.
</div>
