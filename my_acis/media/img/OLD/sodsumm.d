<div id="content">
<textarea rows="50" cols="100" style="background-color:LightBlue;color:DarkBlue;border:1px solid Blue;font-size:20px;">
###########
Sodsumm
###########
This program calculates a general climatology for a site
based on DAILY input data.  Much more detailed information
can be obtained for each climate element by running the
other programs on the menu(s).  Other climate elements such
as snow depth or evaporation are not summarized by this
program

Input:
    Coop Station Id(s)          dddddd, dddddd
    Start date                  yyyy
    End date                    yyyy
    Max Number of Days missing  Gaussian or Running Mean
    Element collections         Temperature (maxt, mint, avgt)
                                Precipitation and Snowfall
                                Temperature and Precip/Snowfall
                                Heating/Cooling Degree Days
                                Growing Degree Days
                                All of the above

Sample Output:

For monthly and annual mean, thresholds and sums:
Month with 5 or more missing days are not considered
Years with one or mor missing months are not considered
Two-didgit years are departures from 1900: -20 = 1880, 102 = 2002
Station: (266779) RENO TAHOE INTL AP
From Year 2000 To Year 2011

Cooling degree days:
Output is rounded, unlike NCDC values, which round input.
Degree Days to selected Base Temperatures(F)

Base    Jan     Feb     Mar     Apr     May     Jun     Jul     Aug     Sep     Oct     Nov     Dec     Ann 
55      0       0       8       36      222     442     705     604     343     76      2       0       2438    
57      0       0       3       21      178     385     643     542     288     50      0       0       2110    
60      0       0       1       9       121     301     550     449     209     24      0       0       1664    
65      0       0       0       1       53      175     396     297     97      5       0       0       1024    
70      0       0       0       0       14      74      246     152     27      1       0       0       514

Notes:

</div>
