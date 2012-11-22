#!/usr/bin/perl
#
# Program to generate Gif output from with data depiction
#  Graphs for 5 elements.  Max. and Min temp., Precip., Snowfall and snowdepth
#  for WWW

use CGI;
use GD;
use Time::localtime;

$numargs = @ARGV;
# Is control file given as an argument
if ($numargs == 1) {
   $stationid = $ARGV[0];
} else {
   # Input data file
   print ("Enter a 6-digit coop id:\n");
   $stationid = <STDIN>;
}

$sdate = 18700101;
#$sdate = 19000101;
$edate = 20121111;
$tm = localtime;
#$testdate = "%04d%02d%02d", $tm->year + 1900, ($tm->mon) + 1, $tm->mday;
#$testdate = int($testdate)

#foreach $stationid (@stationid) {
$stnid = substr($stationid, 0, 6);
print "$stnid \n";
$state = substr($stnid, 0, 2);
    if ($state eq "50") {
       $state = "ak";
    } elsif ($state eq "02") {
       $state = "az";
    } elsif ($state eq "04") {
       $state = "ca";
    } elsif ($state eq "05") {
       $state = "co";
    } elsif ($state eq "51") {
       $state = "hi";
    } elsif ($state eq "10") {
       $state = "id";
    } elsif ($state eq "24") {
       $state = "mt";
    } elsif ($state eq "26") {
       $state = "nv";
    } elsif ($state eq "29") {
       $state = "nm";
    } elsif ($state eq "91") {
       $state = "pi";
    } elsif ($state eq "35") {
       $state = "or";
    } elsif ($state eq "41") {
       $state = "tx";
    } elsif ($state eq "42") {
       $state = "ut";
    } elsif ($state eq "45") {
       $state = "wa";
    } elsif ($state eq "48") {
       $state = "wy";
    } elsif ($state eq "01") {
       $state = "al";
    } elsif ($state eq "03") {
       $state = "ar"; 
    } elsif ($state eq "06") {
       $state = "ct";
    } elsif ($state eq "07") {
       $state = "de";
    } elsif ($state eq "08") {
       $state = "fl";
    } elsif ($state eq "09") {
       $state = "ga";
    } elsif ($state eq "11") {
       $state = "il";
    } elsif ($state eq "12") {
       $state = "in";
    } elsif ($state eq "13") {
       $state = "ia";
    } elsif ($state eq "14") {
       $state = "ks";
    } elsif ($state eq "15") {
       $state = "ky";
    } elsif ($state eq "16") {
       $state = "la";
    } elsif ($state eq "17") {
       $state = "me";
    } elsif ($state eq "18") {
       $state = "md";
    } elsif ($state eq "19") {
       $state = "ma";
    } elsif ($state eq "20") {
       $state = "mi";
    } elsif ($state eq "21") {
       $state = "mn";
    } elsif ($state eq "22") {
       $state = "ms";
    } elsif ($state eq "23") {
       $state = "mo";
    } elsif ($state eq "25") {
       $state = "ne";
    } elsif ($state eq "27") {
       $state = "nh";
    } elsif ($state eq "28") {
       $state = "nj";
    } elsif ($state eq "30") {
       $state = "ny";
    } elsif ($state eq "31") {
       $state = "nc";
    } elsif ($state eq "32") {
       $state = "nd";
    } elsif ($state eq "33") {
       $state = "oh";
    } elsif ($state eq "34") {
       $state = "ok";
    } elsif ($state eq "36") {
       $state = "pa";
    } elsif ($state eq "37") {
       $state = "ri";
    } elsif ($state eq "38") {
       $state = "sc";
    } elsif ($state eq "39") {
       $state = "sd";
    } elsif ($state eq "40") {
       $state = "tn";
    } elsif ($state eq "43") {
       $state = "vt";
    } elsif ($state eq "44") {
       $state = "va";
    } elsif ($state eq "46") {
       $state = "wv";
    } elsif ($state eq "47") {
       $state = "wi";
    } elsif ($state eq "67") {
       $state = "vi";
    } elsif ($state eq "66") {
       $state = "pr";
    } elsif ($state eq "96") {
       $state = "wr";
    } elsif ($state eq "97") {
       $state = "ml";
    } elsif ($state eq "98") {
       $state = "ws";
    }

   $filename = "python /Users/bdaudert/DRI/AcisWS_WRCC_PythonScripts/ws_meta_lister.py -c $stnid -s $sdate -f $edate";
   open(SOD, "$filename|") || die ("Can't retrieve data.\n");
   print "$filename \n";
  #load data
   @soddata = <SOD>;
   @sod2 = sort(@soddata);
   close (SOD);

# Input data from file
@data = <RECDATA>;

# create array for each variable
$count = 0;
$ymx = 2020;
$ymn = 1870;
foreach $sod2(@sod2) {
#   @elem = split(/ +/,$data);
   $year = substr($sod2, 6, 4);
   $mon = substr($sod2, 10, 2);
   $day = substr($sod2, 12, 2);
   $cjday = &jday($mon, $day, 4);
   if ($cjday < 10) {
      $cjday = substr($cjday, 1, 1);
   }
   
#   if ($year ne $yearo) {
#      print "$year \n";
#   }
#   $yearo = $year;

   $pcpn{$cjday,$year-1870} = substr($sod2, 17, 4);
   $pcpnf{$cjday,$year-1870} = substr($sod2, 21, 1);
   $snwf{$cjday,$year-1870} = substr($sod2, 24, 4);
   $snwff{$cjday,$year-1870} = substr($sod2, 28, 1);
   $snwd{$cjday,$year-1870} = substr($sod2, 33, 4);
   $snwdf{$cjday,$year-1870} = substr($sod2, 35, 1);
   $tmax{$cjday,$year-1870} = substr($sod2, 38, 4);
   $tmaxf{$cjday,$year-1870} = substr($sod2, 42, 1);
   $tmin{$cjday,$year-1870} = substr($sod2, 45, 4);
   $tminf{$cjday,$year-1870} = substr($sod2, 49, 1);
}

print $pcpn;

# compute y-axis ratio
if ($ymx != $ymn ) {
   $yratio = 286 / ($ymx - $ymn);
}
#   print ("$yratio $ymx $ymn\n");

# Open GIF Image
$im = new GD::Image(510,433);
$title2 = "Observed Element : Maximum Daily Temperature";

&extra($im);

# Display data
for ($year=1870; $year<=2013; $year++) {
   #print "$tmax{100,$year-1870} \n";
   for ($cjday=1; $cjday<=366; $cjday++) {
      if (($tmax{$cjday,$year-1870} ne '    ')&&($tmax{$cjday,$year-1870} ne '')&&($tmaxf{$cjday,$year-1870} ne "M")) {
         $im->setPixel(70+$cjday,356 - int((($year - $ymn)*$yratio)+0.5),$red);
         $im->setPixel(70+$cjday,357 - int((($year - $ymn)*$yratio)+0.5),$red);
      }
   }
}

# print the image
#print "Content-type: image/gif\n\n";
#print $im->gif;
$dir_path = "/Users/bdaudert/DRI/dj-projects/my_acis/media/img/";

$gif_data = $im->gif;
open (GIFFILE,">" . $dir_path . "tmax.gif") || die ("Can't open tmax.gif");
#open (GIFFILE,">" . $stnid . "tmax.gif") || die ("Can't open $stnidtmax.gif");
print GIFFILE $gif_data;
close GIFFILE;

# Open GIF Image
$im2 = new GD::Image(510,433);
$title2 = "Observed Element : Minimum Daily Temperature";
&extra($im2);

# Display data
for ($year=1870; $year<=2013; $year++) {
   #print "$tmax{100,$year-1870} \n";
   for ($cjday=1; $cjday<=366; $cjday++) {
      if (($tmin{$cjday,$year-1870} ne '    ')&&($tmin{$cjday,$year-1870} ne '')&&($tminf{$cjday,$year-1870} ne "M")) {
         $im2->setPixel(70+$cjday,356 - int((($year - $ymn)*$yratio)+0.5),$red);
         $im2->setPixel(70+$cjday,357 - int((($year - $ymn)*$yratio)+0.5),$red);
      }
   }
}

#print $im2->gif;
$gif_data = $im2->gif;
open (GIFFILE,">" . $dir_path . "tmin.gif") || die ("Can't open tmin.gif");
# open (GIFFILE,">" . $stnid . "tmin.gif") || die;
print GIFFILE $gif_data;
close GIFFILE;

# Open GIF Image
$im3 = new GD::Image(510,433);
$title2 = "Observed Element : Daily Total Precipitation";
&extra($im3);

# Display data
for ($year=1870; $year<=2013; $year++) {
   #print "$tmax{100,$year-1870} \n";
   for ($cjday=1; $cjday<=366; $cjday++) {
      if (($pcpn{$cjday,$year-1870} ne '    ')&&($pcpn{$cjday,$year-1870} ne '')&&($pcpnf{$cjday,$year-1870} ne "M")) {
         $im3->setPixel(70+$cjday,356 - int((($year - $ymn)*$yratio)+0.5),$green);
         $im3->setPixel(70+$cjday,357 - int((($year - $ymn)*$yratio)+0.5),$green);
      }
   }
}

#print $im3->gif;
$gif_data = $im3->gif;
# open (GIFFILE,">" . $stnid . "pcpn.gif") || die;
open (GIFFILE,">" . $dir_path . "pcpn.gif") || die ("Can't open pcpn.gif");
print GIFFILE $gif_data;
close GIFFILE;

# Open GIF Image
$im4 = new GD::Image(510,433);
$title2 = "Observed Element : Daily Total Snowfall";
&extra($im4);

# Display data
for ($year=1870; $year<=2013; $year++) {
   #print "$tmax{100,$year-1870} \n";
   for ($cjday=1; $cjday<=366; $cjday++) {
      if (($snwd{$cjday,$year-1870} ne '    ')&&($snwd{$cjday,$year-1870} ne '')&&($snwdf{$cjday,$year-1870} ne "M")) {
         $im4->setPixel(70+$cjday,356 - int((($year - $ymn)*$yratio)+0.5),$blue);
         $im4->setPixel(70+$cjday,357 - int((($year - $ymn)*$yratio)+0.5),$blue);
      }
   }
}

#print $im4->gif;
$gif_data = $im4->gif;
#open (GIFFILE,">" . $stnid . "snwd.gif") || die;
open (GIFFILE,">" . $dir_path . "snow.gif") || die ("Can't open snow.gif");
print GIFFILE $gif_data;
close GIFFILE;

# Open GIF Image
$im5 = new GD::Image(510,433);
$title2 = "Observed Element : Daily Total Snowdepth";
&extra($im5);

# Display data
for ($year=1870; $year<=2013; $year++) {
   #print "$tmax{100,$year-1870} \n";
   for ($cjday=1; $cjday<=366; $cjday++) {
      if (($snwf{$cjday,$year-1870} ne '    ')&&($snwf{$cjday,$year-1870} ne '')&&($snwff{$cjday,$year-1870} ne "M")) {
         $im5->setPixel(70+$cjday,356 - int((($year - $ymn)*$yratio)+0.5),$blue);
         $im5->setPixel(70+$cjday,357 - int((($year - $ymn)*$yratio)+0.5),$blue);
      }
   }
}

#print $im5->gif;
$gif_data = $im5->gif;
# open (GIFFILE,">" . $stnid . "snwd.gif") || die;
open (GIFFILE,">" . $dir_path . "snwd.gif") || die ("Can't open snwd.gif");
print GIFFILE $gif_data;
close GIFFILE;

# close for loop 
undef (%tmax);
undef (%tmaxf);
undef (%tmin);
undef (%tminf);
undef (%pcpn);
undef (%pcpnf);
undef (%snwd);
undef (%snwdf);
undef (%snwf);
undef (%snwff);

#----------- jday subroutine --------------
sub jday {
   local ($mon, $day, $yr) = @_;
#  print ("$mon $day \n");
   # leap year (every fourth (2000 not applied))
   if (($yr/4) == (int($yr/4))) {
      if ($mon == " 01") {
         $jday = $day;
      } elsif ($mon == " 02") {
         $jday = 31 + $day;
      } elsif ($mon == " 03") {
         $jday = 60 + $day;
      } elsif ($mon == " 04") {
         $jday = 91 + $day;
      } elsif ($mon == " 05") {
         $jday = 121 + $day;
      } elsif ($mon == " 06") {
         $jday = 152 + $day;
      } elsif ($mon == " 07") {
         $jday = 182 + $day;
      } elsif ($mon == " 08") {
         $jday = 213 + $day;
      } elsif ($mon == " 09") {
         $jday = 244 + $day;
      } elsif ($mon == " 10") {
         $jday = 274 + $day;
      } elsif ($mon == " 11") {
         $jday = 305 + $day;
      } elsif ($mon == " 12") {
         $jday = 335 + $day;
      } else {
         print ("julian day conversion error.\n");
      }
   } else {
      if ($mon == " 01") {
         $jday = $day;
      } elsif ($mon == " 02") {
         $jday = 31 + $day;
      } elsif ($mon == " 03") {
         $jday = 59 + $day;
      } elsif ($mon == " 04") {
         $jday = 90 + $day;
      } elsif ($mon == " 05") {
         $jday = 120 + $day;
      } elsif ($mon == " 06") {
         $jday = 151 + $day;
      } elsif ($mon == " 07") {
         $jday = 181 + $day;
      } elsif ($mon == " 08") {
         $jday = 212 + $day;
      } elsif ($mon == " 09") {
         $jday = 243 + $day;
      } elsif ($mon == " 10") {
         $jday = 273 + $day;
      } elsif ($mon == " 11") {
         $jday = 304 + $day;
      } elsif ($mon == " 12") {
         $jday = 334 + $day;
      } else {
         print ("julian day conversion error.\n");
      }
   }
}

#-------subroutines for legends, titles, etc.
sub extra {
   local ($im) = @_;
# allocate colors
# allocate white (also becomes background color)
$white = $im->colorAllocate(255, 255, 255);
# allocate black
$black = $im->colorAllocate(0, 0, 0);
# allocate red
$red = $im->colorAllocate(255, 0, 0);
# allocate green
$green = $im->colorAllocate(0,255,0);
# allocate yellow
$yellow = $im->colorAllocate(255,255,0);
# allocate blue
$blue = $im->colorAllocate(0,0,255);
# allocate gray
$gray = $im->colorAllocate(190,190,190);
# allocate dark gray
$dgray = $im->colorAllocate(158,158,158);

# draw frame and graph area and shade graph area
$im->interlaced('true');
$im->rectangle(0,0,509,432,$black);
$im->rectangle(70,70,437,356,$black);
#$im->fill(100,200,$gray);

# Title
$num = length($title1);
$im->string(gdLargeFont,253-($num * 4),25,$title1,$black);
$num = length($title2);
$im->string(gdMediumBoldFont,253-int($num*3.5),45,$title2,$black);

# X-axis title                                             
$im->string(gdMediumBoldFont,210,383,"Day of Year",$black);

# X-axis legend
$im->string(gdSmallFont,59,361,"Jan 1",$black);
$im->string(gdSmallFont,60 + 32,371,"Feb 1",$black);
$im->string(gdSmallFont,60 + 61,361,"Mar 1",$black);
$im->string(gdSmallFont,60 + 92,371,"Apr 1",$black);
$im->string(gdSmallFont,60 + 122,361,"May 1",$black);
$im->string(gdSmallFont,60 + 153,371,"Jun 1",$black);
$im->string(gdSmallFont,60 + 183,361,"Jul 1",$black);
$im->string(gdSmallFont,60 + 214,371,"Aug 1",$black);
$im->string(gdSmallFont,60 + 245,361,"Sep 1",$black);
$im->string(gdSmallFont,60 + 275,371,"Oct 1",$black);
$im->string(gdSmallFont,60 + 306,361,"Nov 1",$black);
$im->string(gdSmallFont,60 + 336,371,"Dec 1",$black);
$im->string(gdSmallFont,60 + 365,361,"Dec 31",$black);

# Y-axis left title
$im->stringUp(gdMediumBoldFont,20,270,"       Year    ",$black);

# Y-axis left legend
$ileft = 0;
$intleft = $ymx - $ymn;
$label = $ymn;
while ($ileft <= $intleft) {
   while (length($label) < 3) { $label = " " .$label; }
   $im->string(gdTinyFont,46,351 - int($ileft*$yratio),"$label",$black);
   $ileft = $ileft + 10;
   $label = $label + 10;
}

# X-axis Grid
$ileft = 0;
$intleft = $ymx - $ymn;
while ($ileft < $intleft) {
   $im->line(439,356 - int($ileft*$yratio),68,356 - int($ileft*$yratio),$dgray);   $ileft = $ileft + 10;
   $label = $label + 10;
}

# Y-axis Grid
$im->dashedLine(70 + 32,70,70 + 32,356,$dgray);
$im->dashedLine(70 + 61,70,70 + 61,356,$dgray);
$im->dashedLine(70 + 92,70,70 + 92,356,$dgray);
$im->dashedLine(70 + 122,70,70 + 122,356,$dgray);
$im->dashedLine(70 + 153,70,70 + 153,356,$dgray);
$im->dashedLine(70 + 183,70,70 + 183,356,$dgray);
$im->dashedLine(70 + 214,70,70 + 214,356,$dgray);
$im->dashedLine(70 + 245,70,70 + 245,356,$dgray);
$im->dashedLine(70 + 275,70,70 + 275,356,$dgray);
$im->dashedLine(70 + 306,70,70 + 306,356,$dgray);
$im->dashedLine(70 + 336,70,70 + 336,356,$dgray);

# Write WRCC id
$im->string(gdTinyFont,460,390,"Western",$black);
$im->string(gdTinyFont,458,400,"Regional",$black);
$im->string(gdTinyFont,460,410,"Climate",$black);
$im->string(gdTinyFont,463,420,"Center",$black);

}

