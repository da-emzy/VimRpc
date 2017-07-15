#!/usr/bin/env perl
use strict;
use warnings;
use Android;
my $tty = Android->new();
my $ret = $tty->curWinData()->{'Result'};
print($ret);
