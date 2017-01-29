<div id="content">
<textarea rows="50" cols="100" style="background-color: LightBlue;color:DarkBlue;border:1px solid Blue;font-size:20px;">
###########
Soddyrec
###########
This program will determine means and extremes for any averaging period desired.

Input:
    Coop Station Id(s)    dddddd, dddddd
    Start date            yyyymmdd
    End date              yyyymmdd
    Element combinations  [pcpn, snow, snwd, maxt, mint, hdd, cdd]
                          [maxt, mint, pcpn]
                          [pcpn, snow, snwd]
                          or each individually
                          [hdd]
                          [cdd]


Sample Output:
   AVE  Multi year unsmoothed average of the indicated quantity
   HI Highest value of the indicated quantity for this day of the year
   LO Lowest value of the indicated quantity for this day of the year
   YR Latest year of occurrence of the extreme value
   NO Number of years with data for this day of year 


    Example Output Tables
    Station Id | Station Name
    |------Precipitation------|             
     MO DAY    AVE    NO  HIGH   YR         
     1    1  0.345    10  1.32 2001         
     1    2  0.467    10  1.56 1895

    |----------MAXT----------|
     MO DAY     AVE    NO  HIGH   YR LOW   YR
      2  28      55    24    80 1898  34 2000
      2  29      67     6    87 1972  44 1983
      3   1      75    24    90 1965  55 1976 
Notes:
    for maxt and mint we will also report high lows and low highs
    Units: Inches and degrees Fahrenheit
    precip measured in hundredths  of inches --> averages for precip have 3 decimal place precision 
    snow measured in tenth of inches --> averages for snow have 2 decimal place precision 
    snwd, temps and dd are measured in whole units --> no decimal places for averages 
</div>
