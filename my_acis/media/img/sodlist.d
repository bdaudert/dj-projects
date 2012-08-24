<div id="content">
<textarea rows="50" cols="100" style="background-color: LightBlue;color:DarkBlue;border:1px solid Blue;font-size:20px;">
###########
Sodlist
###########
This program is a data lister. 
It will list pcpn, snow, snwd, maxt, mint (, tobs, evap) data
over a period given by a start date and end date. If the user is 
only interested in data spanning part of the year (e.g. a season), a window 
can be defined to isolate that interval.

Input:
    Coop Station Id(s) dddddd, dddddd
    Start date         yyyymmdd
    End date           yyyymmdd
    Otput Format       json, csv, ascii
    Start Window       mmdd (default = 0101)
    End Window         mmdd (default = 1231)
    Minimize           Leave out station number abd 5 spaces on each line (default = False)
    Include Tobs Evap  Include temperature at observation and evap data (default =  False)

Output:

Notes:
    units: 
        maxt, mint, avgt, dtr, mmt=min/maxtemps, cdd, hdd: tenth degrees F/C (default F)
        pcpn, evap: hundredths of inches
        snow: tenth of inches
        snwd: whole inches
        awnd: whole miles per day
        wesf=water estimate snow fall: tenth of inches
</div>
