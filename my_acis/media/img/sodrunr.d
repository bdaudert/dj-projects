###########
Sodrun
###########
This program finds all runs of consecutive days where requested
threshold conditions are met or exceeded.  It considers 2 days at a time.
The conditions apply only to a single climate element at a time.
Starting and ending day of all runs greater than a specified 
length are printed.  Runs are not
allowed to cross a missing day; user is informed of all missing days
that may possibly interrupt runs. Only runs with at least one occurrence
are reported.

Input:
    Coop Station Id(s) dddddd, dddddd
    Start date yyyymmdd
    End date   yyyymmdd
    Element    e.g. pcpn
    Aeb        above, below or equal
    Threshold  integer threshold value
    Min Run    number of days in a run to be reported
    Verbose    if turned on it will return information about data where
               the threshold was not met
Output:

    Output Sample

    ========================================================================
    STATION : COOP_STATION_ID : 266779 NAME : RENO TAHOE INTL AP STATE : NV
    RUNS OF TMAX >
    START: 20120501 END: 20120703
    MINIMUM DURATION 1

    TMAX > 70 START : 20120501 END : 20120503 2 DAYS
    TMAX > 70 START : 20120507 END : 20120525 18 DAYS
    TMAX > 70 START : 20120528 END : 20120605 8 DAYS
    TMAX > 70 START : 20120607 END : 20120609 2 DAYS
    TMAX > 70 START : 20120610 END : 20120703 23 DAYS
    1 DAYS MISSING  NEXT DATE : 20120703
    DAYS NUMBER_OF_RUNS
    2    2
    8    1
    18   1
    23   1

Notes:
    A,S and T flagged data at the beginning or the end of a streak are ignored.
    If an A,S or T flag is encountered in the middle of a streak, the streak is interrupted.
    If missing data is encountered in the middle of a streak, the streak is interrupted.

