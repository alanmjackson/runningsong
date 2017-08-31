#!/usr/bin/perl
# bjohas.de, March 2017
# Convert kml into csv, containing arches for Alan's runs.

    
use XML::LibXML;
use XML::LibXML::XPathContext;

if ($ARGV[0] eq "") {
    die("Provide kml file as input.");
};

open F,"$ARGV[0]";
$f = join "",<F>;
close F;

open F,">$ARGV[0].csv";
print F "name\td (m)\tv1\tv2\tangle1 (deg)\tangle2 (deg)\ttrackpoints\n";

my $dom = XML::LibXML->load_xml(location => $ARGV[0]);
my $xpc = XML::LibXML::XPathContext->new($dom);
$xpc->registerNs('kml',  'http://www.opengis.net/kml/2.2');

foreach my $placemark ($xpc->findnodes('//kml:Placemark')) {
    # print $placemark;
    $name = $xpc->findvalue('./kml:name', $placemark) || 'undefined';
    ($arch = $name) =~ s/^(\d+)\D.*/$1/gs;
    $coords = $xpc->findnodes('./kml:LineString/kml:coordinates', $placemark);
    $c = $coords->to_literal();
    $c =~ s/^\s+//sg;
    $c =~ s/\s+$//sg;
    $c =~ s/\s+/ /sg;
    @c = split / /,$c;
    $arcnumber = $arcnumber + 1;
    $d = &distancesum(@c);
    $angle1 = &bear($c[0],$c[1]);
    $angle2 = &bear($c[$#c],$c[$#c-1]);
    if (!defined $n{$c[0]}) {
	$n++;
	$n{$c[0]} = $n;
    };
    if (!defined $n{$c[$#c]}) {
	$n++;
	$n{$c[$#c]} = $n;
    };
    use Math::Round;

    $d = round($d);
    $angle1 = round($angle1);
    $angle2 = round($angle2);
    while (length($n{$c[0]})<3) {$n{$c[0]} = "0" . $n{$c[0]} };
    while (length($n{$c[$#c]})<3) {$n{$c[$#c]} = "0" . $n{$c[$#c]} };
    print F "a$arcnumber\t$d\tv$n{$c[0]}\tv$n{$c[$#c]}\t$angle1\t$angle2\t$c\n";

    $v{$n{$c[0]}}{p} = $c[0];
    $v{$n{$c[0]}}{a}{"a$arch"} = 1;

    $v{$n{$c[$#c]}}{p} = $c[0];
    $v{$n{$c[$#c]}}{a}{"a$arch"} = 1;


#    print "OUT $n\t$d\t$angle1\t$angle2\n\n\n";
};
close F;


open F,">$ARGV[0]-v.csv";
print F "vertex\td (m)\tv1\tv2\tangle1 (deg)\tangle2 (deg)\twaypoins\n";
foreach $v (sort keys %v) {
    $a = join " ",sort keys %{$v{$v}{a}};
    print F "v$v\t$v{$v}{p}\t$a\n";
};


sub lalo() {
    my ($lon1,$lat1) = split ",",$_[0];
    return ($lat1, $lon1);
};


sub distancesum() {
#    print "d=".&distance(@ARGV)," m\n";
#    print "b=".&bearing(@ARGV)," deg\n";
    my @a = @_;
    my $i = 0;
#    foreach (@a[1..$#a]) {
    my $d = 0;
    for ($i=1;$i<=$#a;$i++) {
	$d += &dist($a[$i-1],$a[$i]);
    };
    return $d;
};

sub bear() {
    my ($lon1,$lat1) = split ",",$_[0];
    my ($lon2,$lat2) = split ",",$_[1];
    return &bearing($lat1, $lon1,$lat2, $lon2);
};

sub bearing() {
    my ($lat1, $lon1, $lat2, $lon2) = @_;
    my $pi = 3.14159265359;
    my $rad = $pi/180;
    $lat1 *= $rad;
    $lat2 *= $rad;
    $lon1 *= $rad;
    $lon2 *= $rad;    
    my $y = sin($lon2-$lon1) * cos($lat2);
    my $x = cos($lat1)* sin($lat2) - sin($lat1) * cos($lat2) * cos($lat2-$lat1);
    my $brng = atan2($y, $x) / $rad;
#    print "1 ($lat1, $lon1, $lat2, $lon2) $y, $x, $brng\n";
    return $brng;
};

sub dist() {
    my ($lon1,$lat1) = split ",",$_[0];
    my ($lon2,$lat2) = split ",",$_[1];
#    print "- dis $_[0]; $_[1] => distance($lat1, $lon1, $lat2, $lon2)\n";
    return &distance($lat1, $lon1,$lat2, $lon2);
};

sub distance() {
    my ($lat, $lon, $lat2, $lon2) = @_;
    my $pi = 3.14159265359;
    my $rad = $pi/180;
    my $dx = ($lon - $lon2)*$rad * cos(($lat + $lat2)/2*$rad);
    my $dy = ($lat - $lat2)*$rad ;
    my $dd = ($dx**2 + $dy**2)**0.5 * 6371 * 1000;
#    print "- distance($lat, $lon, $lat2, $lon2) = $dd m\n";
    return $dd;
};


