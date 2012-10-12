<div id="content">
<textarea rows="50" cols="100" style="background-color: LightBlue;color:DarkBlue;border:1px solid Blue;font-size:20px;">
###########
Sodxtrmts
###########
This program produces monthly and annual time series of a large number 
of properties derived from the SOD daily data set.
The user chooses an analysis type from these options:
Monthly Maximimun (mmax), 
Monthly Minimum (mmin), 
Monthly Averages (mave), 
Standard Deviation(sd), 
Number of Days (ndays), 
Range during Month(rmon),
Monthly Sum (msum)
If desired an additional frequency analysis is performed. 
Choices of frequency analyses are:
Pearson III, GEV, Censored Gamma, and possibly Beta-P

Input:
    Coop Station Id(s)          dddddd, dddddd
    Start date                  yyyy
    End date                    yyyy
    Element                     e.g. temperature related elements (maxt, mint)      
    Analysis Type               e.g. Monthly Averages
    Maximum Missing Days allowed 
    Start Month
    Departure from averages     True or False
    Frequency analysis          e.g. Pearson III
    Base Temperature            (if element is heating/cooling/growing degree days) 

Sample Output:
    
    LOCATION:RENO TAHOE INTL AP  STATION: 266779
    START YEAR 2000 END YEAR 2011
    START MONTH 01
    ELEMENT maxt UNITS 
    ANALYSIS TYPE mave
    MAXIMUM NUMBER OF DAYS ALLOWED MISSING 5
    FREQUENCY ANALYSIS T
    DEPARTURES FROM AVERAGES 

    a = 1 day missing, b = 2 days missing, c = 3 days, ..etc..,
    z = 26 or more days missing, A = Accumulations present 
    Long-term means based on columns; thus, the monthly row may not
    sum (or average) to the long-term annual value.

    YEARS   JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC ANN
    2000    48.71   51.41   58.97   69.00   74.90   88.27   90.97   90.90   80.90   66.81   50.10   49.87   68.40
    2001    44.29   47.36   62.45   61.60   83.00   86.03   90.65   94.87   85.47   74.94   57.40   44.68   69.39
    2002    45.55   54.43   56.32   65.73   73.87   86.90   95.68   89.90   83.20   68.61   56.63   48.10   68.74
    2003    55.42   49.68   59.90   56.87   74.84   88.07   96.74   90.00   85.50   76.19   51.57   46.71   69.29
    2004    46.74   48.14   66.71   67.73   75.52   86.80   94.48   90.19   82.77   65.58   51.60   45.71   68.50
    2005    36.00   46.46   59.16   61.70   72.16   78.63   96.55   92.19   78.93   70.00   58.67   47.23   66.47
    2006    48.16   52.54   49.29   61.87   77.19   88.30   95.90   90.71   82.53   67.94   56.43   46.16   68.09
    2007    44.55   52.82   64.65   66.30   79.23   89.00   96.94   93.16   79.33   66.32   58.10   43.26   69.47
    2008    40.58   50.76   58.19   64.10   72.61   85.90   94.87   93.68   85.63   70.26   59.10   46.42   68.51
    2009    50.29   50.93   56.16   64.03   79.71   79.03   94.19   90.06   86.77   65.81   57.80   36.81   67.63
    2010    45.71   50.79   57.23   60.13   65.68   82.63   94.29   88.94   85.73   68.10   52.63   48.97   66.74
    MEAN    46.00   50.48   59.00   63.55   75.34   85.42   94.66   91.33   83.34   69.14   55.46   45.81   68.29
    S.D.     5.04    2.42    4.66    3.56    4.58    3.68    2.14    1.87    2.73    3.54    3.30    3.52    1.01
    SKW10   -0.18   -0.19   -0.30   -0.21   -0.39   -1.00   -0.90   0.66    -0.41   1.01    -0.50   -1.52   -0.62
    MAX     55.42   54.43   66.71   69.00   83.00   89.00   96.94   94.87   86.77   76.19   59.10   49.87   69.47
    MIN     36.00   46.46   49.29   56.87   65.68   78.63   90.65   88.94   78.93   65.58   50.10   36.81   66.47
    YEARS   11.00   11.00   11.00   11.00   11.00   11.00   11.00   11.00   11.00   11.00   11.00   11.00   11.00

    
Notes:
</div>
