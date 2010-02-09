#!/usr/bin/perl -w

$f1 = shift @ARGV;
$f2 = shift @ARGV;

open F1, "<$f1";
open F2, "<$f2";
while(<F1>) {
    chop;
    $l2 = <F2>;
    chop $l2;
    print "$_ $l2\n";
}

