#!/usr/bin/env perl

use strict;
use warnings;

use Frontier::Client;

# testing
print "connecting to server \n";
my $s_url = 'http://127.0.0.1:1700';
print "address initiated \n";
my $server = Frontier::Client->new(url => $s_url);
print "connecting to $server \n";
my $result = $server->call('getLine',10);
print "connected.... \n";
# my $dict = $result->{'Result'};
print "RESULT $result \n";
