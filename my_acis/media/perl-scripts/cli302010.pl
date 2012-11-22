#!/usr/local/bin/perl
#
#  Program to generate GIF output from soddynorm table
#  for WWW

use GD;

# Input data file
#print ("Enter the name of the output file from soddynorm:\n");
#$filename = <STDIN>;
#chop ($filename);

$filename = $ARGV[0];

# Do some checking on the input string
# ie.  restrict acceptable access
#
$state = substr($filename, 0, 2);
$found = 0;
if ($state eq "ak") {
    $found = 1;
} elsif ($state eq "az") {
    $found = 1;
} elsif ($state eq "ca") {
    $found = 1;
} elsif ($state eq "co") {
    $found = 1;
} elsif ($state eq "hi") {
    $found = 1;
} elsif ($state eq "id") {
    $found = 1;
} elsif ($state eq "mt") {
    $found = 1;
} elsif ($state eq "nm") {
    $found = 1;
} elsif ($state eq "nv") {
    $found = 1;
} elsif ($state eq "or") {
    $found = 1;
} elsif ($state eq "pi") {
    $found = 1;
} elsif ($state eq "tx") {
    $found = 1;
} elsif ($state eq "ut") {
    $found = 1;
} elsif ($state eq "wa") {
    $found = 1;
} elsif ($state eq "wy") {
    $found = 1;
} elsif (($state eq "al") || ($state eq "ar") || ($state eq "ct") || ($state eq "de")) {
    $found = 1;
} elsif (($state eq "fl") || ($state eq "ga") || ($state eq "il") || ($state eq "in")) {
    $found = 1;
} elsif (($state eq "ia") || ($state eq "ks") || ($state eq "ky") || ($state eq "la")) {
    $found = 1;
} elsif (($state eq "me") || ($state eq "md") || ($state eq "ma") || ($state eq "mn")) {
    $found = 1;
} elsif (($state eq "mi") || ($state eq "mo") || ($state eq "ms") || ($state eq "ne")) {
    $found = 1;
} elsif (($state eq "nh") || ($state eq "nj") || ($state eq "ny") || ($state eq "nc")) {
    $found = 1;
} elsif (($state eq "nd") || ($state eq "oh") || ($state eq "ok") || ($state eq "pa")) {
    $found = 1;
} elsif (($state eq "ri") || ($state eq "sc") || ($state eq "sd") || ($state eq "tn")) {
    $found = 1;
} elsif (($state eq "tx") || ($state eq "vt") || ($state eq "va") || ($state eq "wv")) {
    $found = 1;
} elsif (($state eq "wi") || ($state eq "vi") || ($state eq "pr")) {
    $found = 1;
}
if ($found != 1) {
    exit(0); 
}

$filename = "/hurr4/www/clim/" . $state . "/" . $filename;

# begin html output
print "Content-type: image/gif\n\n";

# Input Station Name
#print ("Enter the name of the station:\n");
#$station = <STDIN>;
#chop ($station);

# Get Graph first title from .rec file
unless (open(RECDATA, $filename . ".rec")) {
   if (!(-e $filename)) {
      die ("File $filename does not exist.\n");
   } elsif (!(-r $filename)) {
      die ("You are not allowed to read $filename.\n");
   } else {
      die ("File $filename can not be opened.\n");
   }
}
# input first line
$line = <RECDATA>;
$Stnname = substr($line, 35, 27);
$Stnname =~ s/[\t ]+$//;
$Stnid = substr($line, 27, 6);
$State = substr($line, 69, 2);
if ($State eq "ak") { $State = "ALASKA"; }
if ($State eq "al") { $State = "ALABAMA"; }
if ($State eq "az") { $State = "ARIZONA"; }
if ($State eq "ar") { $State = "ARKANSAS"; }
if ($State eq "ca") { $State = "CALIFORNIA"; }
if ($State eq "co") { $State = "COLORADO"; }
if ($State eq "ct") { $State = "CONNECTICUT"; }
if ($State eq "de") { $State = "DELAWARE"; }
if ($State eq "fl") { $State = "FLORIDA"; }
if ($State eq "ga") { $State = "GEORGIA"; }
if ($State eq "hi") { $State = "HAWAII"; }
if ($State eq "id") { $State = "IDAHO"; }
if ($State eq "il") { $State = "ILLINOIS"; }
if ($State eq "in") { $State = "INDIANA"; }
if ($State eq "ia") { $State = "IOWA"; }
if ($State eq "ks") { $State = "KANSAS"; }
if ($State eq "ky") { $State = "KENTUCKY"; }
if ($State eq "la") { $State = "LOUISIANA"; }
if ($State eq "me") { $State = "MAINE"; }
if ($State eq "md") { $State = "MARYLAND"; }
if ($State eq "ma") { $State = "MASSACHUSETTS"; }
if ($State eq "mi") { $State = "MICHIGAN"; }
if ($State eq "mn") { $State = "MINNESOTA"; }
if ($State eq "ms") { $State = "MISSISSIPPI"; }
if ($State eq "mo") { $State = "MISSOURI"; }
if ($State eq "mt") { $State = "MONTANA"; }
if ($State eq "ne") { $State = "NEBRASKA"; }
if ($State eq "nv") { $State = "NEVADA"; }
if ($State eq "nh") { $State = "NEW HAMPSHIRE"; }
if ($State eq "nj") { $State = "NEW JERSEY"; }
if ($State eq "nm") { $State = "NEW MEXICO"; }
if ($State eq "ny") { $State = "NEW YORK"; }
if ($State eq "nc") { $State = "NORTH CAROLINA"; }
if ($State eq "nd") { $State = "NORTH DAKOTA"; }
if ($State eq "oh") { $State = "OHIO"; }
if ($State eq "ok") { $State = "OKLAHOMA"; }
if ($State eq "or") { $State = "OREGON"; }
if ($State eq "pi") { $State = "PACIFIC OCEAN"; }
if ($State eq "pa") { $State = "PENNSYLVANIA"; }
if ($State eq "pr") { $State = "PUERTO RICO"; }
if ($State eq "ri") { $State = "RHODE ISLAND"; }
if ($State eq "sc") { $State = "SOUTH CAROLINA"; }
if ($State eq "sd") { $State = "SOUTH DAKOTA"; }
if ($State eq "tn") { $State = "TENNESSEE"; }
if ($State eq "tx") { $State = "TEXAS"; }
if ($State eq "ut") { $State = "UTAH"; }
if ($State eq "vt") { $State = "VERMONT"; }
if ($State eq "va") { $State = "VIRGINIA"; }
if ($State eq "vi") { $State = "VIRGIN ISLANDS"; }
if ($State eq "wa") { $State = "WASHINGTON"; }
if ($State eq "wv") { $State = "WEST VIRGINIA"; }
if ($State eq "wi") { $State = "WISCONSIN"; }
if ($State eq "wy") { $State = "WYOMING"; }

$title1 = $Stnname . ", " . $State . "   (" . $Stnid . ")";
close (RECDATA);

# Check for input file and opening 
unless (open(NORMDATA, $filename . ".10n")) {
   if (!(-e $filename)) {
      die ("File $filename does not exist.\n");
   } elsif (!(-r $filename)) {
      die ("You are not allowed to read $filename.\n");
   } else {
      die ("File $filename can not be opened.\n");
   }
}

# Input file header lines
$line = <NORMDATA>;
$line = <NORMDATA>;
$line = <NORMDATA>;
$line = <NORMDATA>;
#   print ("$line\n");

# Input data from file
@data = <NORMDATA>;
close (NORMDATA);

# create array for each variable
$count = 0;
$ryscale = 1;
$lymax = 110;
$lymin = 0;
foreach $data(@data) {
   @elem = split(/ +/,$data);
   $mxt[$count] = $elem[4];
   if ($mxt[$count] > $lymax) {
      $lymin = $lymin + 5;
      $lymax = $lymax + 5;
   }
   $mnt[$count] = $elem[6];
   if ($mnt[$count] < $lymin) {
      $lymin = $lymin - 5;
      $lymax = $lymax - 5;
   }
   $avt[$count] = (($elem[6] + $elem[4]) / 2);
   $pre[$count] = $elem[8];
   if ($pre[$count] > .55 && $ryscale < 2) {
      $ryscale = 2;
   }
   if ($pre[$count] > 1.1 && $ryscale < 3) {
      $ryscale = 3;
   }
#   print ("$mxt[$count] $avt[$count]\n");
   $count++;
}

# Open GIF Image
$im = new GD::Image(510,290);

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
$gray = $im->colorAllocate(191,191,191);
# allocate dark gray
$dgray = $im->colorAllocate(207,207,207);

# draw frame and graph area and shade graph area
$im->interlaced('true');
$im->rectangle(0,0,509,289,$black);
$im->rectangle(70,70,437,213,$black);
$im->fill(100,200,$gray);

# Text
# Title
$num = length ($title1);
$im->string(gdLargeFont,253-($num * 4),25,$title1,$black);
$im->string(gdMediumBoldFont,175,45,"1981-2010 30 Year Average",$black);

# X-axis title                                             
$im->string(gdMediumBoldFont,210,240,"Day of Year",$black);

# X-axis legend
$im->string(gdSmallFont,59,218,"Jan 1",$black);
$im->string(gdSmallFont,60 + 32,228,"Feb 1",$black);
$im->string(gdSmallFont,60 + 61,218,"Mar 1",$black);
$im->string(gdSmallFont,60 + 92,228,"Apr 1",$black);
$im->string(gdSmallFont,60 + 122,218,"May 1",$black);
$im->string(gdSmallFont,60 + 153,228,"Jun 1",$black);
$im->string(gdSmallFont,60 + 183,218,"Jul 1",$black);
$im->string(gdSmallFont,60 + 214,228,"Aug 1",$black);
$im->string(gdSmallFont,60 + 245,218,"Sep 1",$black);
$im->string(gdSmallFont,60 + 275,228,"Oct 1",$black);
$im->string(gdSmallFont,60 + 306,218,"Nov 1",$black);
$im->string(gdSmallFont,60 + 336,228,"Dec 1",$black);
$im->string(gdSmallFont,60 + 365,218,"Dec 31",$black);

# Y-axis left title
$im->stringUp(gdMediumBoldFont,20,200,"Temperature (F)",$black);

# Y-axis left legend
for ($lcount=0; $lcount<12; $lcount++) {
  $legend = ($lcount * 10) + $lymin;
  while (length($legend) < 3) { $legend = " " . $legend; }
  $im->string(gdTinyFont,50,65 + 143 - ($lcount * 13),"$legend",$black);
}
#$im->string(gdTinyFont,50,65,"110",$black);
#$im->string(gdTinyFont,50,65 + 13,"100",$black);
#$im->string(gdTinyFont,50,65 + 26," 90",$black);
#$im->string(gdTinyFont,50,65 + 39," 80",$black);
#$im->string(gdTinyFont,50,65 + 52," 70",$black);
#$im->string(gdTinyFont,50,65 + 65," 60",$black);
#$im->string(gdTinyFont,50,65 + 78," 50",$black);
#$im->string(gdTinyFont,50,65 + 91," 40",$black);
#$im->string(gdTinyFont,50,65 + 104," 30",$black);
#$im->string(gdTinyFont,50,65 + 117," 20",$black);
#$im->string(gdTinyFont,50,65 + 130," 10",$black);
#$im->string(gdTinyFont,50,65 + 143,"  0",$black);

# Y-axis right title
$im->stringUp(gdMediumBoldFont,475,200,"Precipitation (in.)",$black);

# Y-axis right legend
for ($lcount=0; $lcount<12; $lcount++) {
  $legend = $lcount * (0.05 * $ryscale);
  if (length($legend) < 2) { $legend = $legend . "."; }
  while (length($legend) < 4) { $legend = $legend . "0"; }
  $im->string(gdTinyFont,440,65 + 143 - ($lcount * 13),"$legend",$black);
}
#$im->string(gdTinyFont,440,65,"0.55",$black);
#$im->string(gdTinyFont,440,65 + 13,"0.50",$black);
#$im->string(gdTinyFont,440,65 + 26,"0.45",$black);
#$im->string(gdTinyFont,440,65 + 39,"0.40",$black);
#$im->string(gdTinyFont,440,65 + 52,"0.35",$black);
#$im->string(gdTinyFont,440,65 + 65,"0.30",$black);
#$im->string(gdTinyFont,440,65 + 78,"0.25",$black);
#$im->string(gdTinyFont,440,65 + 91,"0.20",$black);
#$im->string(gdTinyFont,440,65 + 104,"0.15",$black);
#$im->string(gdTinyFont,440,65 + 117,"0.10",$black);
#$im->string(gdTinyFont,440,65 + 130,"0.05",$black);
#$im->string(gdTinyFont,440,65 + 143,"0.00",$black);

# X-axis Grid
$im->line(437,70 + 13,70,70 + 13,$dgray);
$im->line(437,70 + 26,70,70 + 26,$dgray);
$im->line(437,70 + 39,70,70 + 39,$dgray);
$im->line(437,70 + 52,70,70 + 52,$dgray);
$im->line(437,70 + 65,70,70 + 65,$dgray);
$im->line(437,70 + 78,70,70 + 78,$dgray);
$im->line(437,70 + 91,70,70 + 91,$dgray);  
$im->line(437,70 + 104,70,70 + 104,$dgray);
$im->line(437,70 + 117,70,70 + 117,$dgray);
$im->line(437,70 + 130,70,70 + 130,$dgray);


# Y-axis Grid
$im->dashedLine(70 + 32,70,70 + 32,213,$dgray);
$im->dashedLine(70 + 61,70,70 + 61,213,$dgray);
$im->dashedLine(70 + 92,70,70 + 92,213,$dgray);
$im->dashedLine(70 + 122,70,70 + 122,213,$dgray);
$im->dashedLine(70 + 153,70,70 + 153,213,$dgray);
$im->dashedLine(70 + 183,70,70 + 183,213,$dgray);
$im->dashedLine(70 + 214,70,70 + 214,213,$dgray);
$im->dashedLine(70 + 245,70,70 + 245,213,$dgray);
$im->dashedLine(70 + 275,70,70 + 275,213,$dgray);
$im->dashedLine(70 + 306,70,70 + 306,213,$dgray);
$im->dashedLine(70 + 336,70,70 + 336,213,$dgray);


# Legends Box
$im->arc(80,265,10,10,180,270,$black);
$im->line(80,260,425,260,$black);
$im->arc(425,265,10,10,270,360,$black);
$im->line(430,265,430,280,$black);
$im->arc(425,280,10,10,0,90,$black);
$im->line(425,285,80,285,$black);
$im->arc(80,280,10,10,90,180,$black);
$im->line(75,280,75,265,$black);
$im->fill(100,270,$gray);

# Write Legends
$im->string(gdSmallFont,105,267,"Max Temp",$black);
$im->string(gdSmallFont,185,267,"Ave Temp",$black);
$im->string(gdSmallFont,265,267,"Min Temp",$black);
$im->string(gdSmallFont,350,267,"Precipitation",$black);
$im->line(80,272,100,272,$red);
$im->line(160,272,180,272,$yellow);
$im->line(240,272,260,272,$blue);
$im->line(325,272,345,272,$green);

# Write WRCC id
$im->string(gdTinyFont,460,250,"Western",$black);
$im->string(gdTinyFont,458,260,"Regional",$black);
$im->string(gdTinyFont,460,270,"Climate",$black);
$im->string(gdTinyFont,463,280,"Center",$black);


# Display data
$count = 0;
while ($count < 365) {
   $im->line(71 + $count,213 - int((($mxt[$count]-$lymin)*1.3)+0.5) ,72 + $count,213 - int((($mxt[$count+1]-$lymin)*1.3)+0.5) ,$red);
   $im->line(71 + $count,213 - int((($avt[$count]-$lymin)*1.3)+0.5) ,72 + $count,213 - int((($avt[$count+1]-$lymin)*1.3)+0.5) ,$yellow);
   $im->line(71 + $count,213 - int((($mnt[$count]-$lymin)*1.3)+0.5) ,72 + $count,213 - int((($mnt[$count+1]-$lymin)*1.3)+0.5) ,$blue);
   $im->line(71 + $count,213 - int(($pre[$count]*(260/$ryscale))+0.5) ,72 + $count,213 - int(($pre[$count+1]*(260/$ryscale))+0.5) ,$green);
#   $mxt[$count] = $elem[4];
#   $mnt[$count] = $elem[6];
#   $avt[$count] = (($elem[6] + $elem[4]) / 2);
#   $pre[$count] = $elem[8];
#   print ("$mxt[$count] $avt[$count]\n");
   $count++;
}
 
# print the image
print $im->gif;
# $gif_data = $im->gif;
#open (GIFFILE,">image.gif") || die;
#print GIFFILE $gif_data;
#close GIFFILE;

