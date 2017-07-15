package Vimclientjson;

use strict;

use vars qw($VERSION $AUTOLOAD);

$VERSION = 0.003;

use IO::Socket;
use JSON;
use Getopt::Long;
use Data::Dumper;

my %Opt;

sub new {
    my $class = shift;
    if (@_) {
        print STDERR "$0: client: new() expected no arguments, got @_\n";
    }
    my $fh = IO::Socket::INET->new(Proto    => 'tcp',
                                   PeerAddr => "127.0.0.1", # $Opt{host},
                                   PeerPort => 1700)
        or die "$0: Cannot connect to server port $Opt{port} on localhost\n";
    $fh->autoflush(1);
    if ($Opt{trace}) {
        show_trace(qq[Android: server in port $Opt{port}]);
    }
    my $self = bless {
        conn => $fh,
        id   => 0,
    }, $class;
    # $self->_authenticate($Opt{handshake});
    return $self;
}


# The connection is implicitly closed when the proxy object goes out
# of scope, but one can use the close() method to explicitly terminate
# the connection.  This is also used internally by the do_rpc() in
# case the server end looks to have gone away.  The _close() closes
# the connection quietly, close() closes the connection noisily.
sub _close {
    if (defined $_[0]->{conn}) {
        close($_[0]->{conn});
        undef $_[0]->{conn};
    }
}
sub close {
    my $self = shift;
    $self->_close();
    print STDERR "$0: client: connection closed\n";
}

# Given a method and parameters, call the server with JSON,
# and return the parsed the response JSON.  If the server side
# looks to be dead, close the connection and return undef.
sub do_rpc {
    my $self = shift;
    if ($self->trace) {
        show_trace(qq[do_rpc: $self: @_]);
    }
    my $method = pop;
    my $DATA_V = 8124;
    my $request = to_json({ id => $self->{id},
                            method => $method,
                            arg => [ @_ ] });
    if (defined $self->{conn}) {
        binmode($self->{conn}, "utf8");
        print { $self->{conn} } $request, "\n";
        if ($self->trace) {
            show_trace(qq[client: sent: "$request"]);
        }
        $self->{id}++;
        my $response;
        my $count = recv($self->{conn}, $response, $DATA_V, 0);
        chomp $response;
        if ($self->trace) {
            show_trace(qq[client: rcvd: "$response"]);
        }
        if (defined $response && length $response) {
            my $result = from_json($response);
            my $success = 0;
            my $error;
            if (defined $result) {
                if (ref $result eq 'HASH') {
                    if (defined $result->{Error}) {
                        $error = to_json( { Error => $result->{Error} } );
                    } else {
                        $success = 1;
                    }
                } else {
                    $error = "illegal JSON reply: $result";
                }
            }
            unless ($success || defined $error) {
                $error = "unknown JSON error";
            }
            if (defined $error) {
                printf STDERR "$0: client: error: %s\n", $error;
            }
            if ($Opt{trace}) {
                print STDERR Data::Dumper->Dump([$result], [qw(result)]);
            }
            return $result;
        }
    }
    $self->close;
    return;
}

# Return stubs that call do_rpc() with the method name smuggled in.
sub rpc_maker {
    if ($Opt{trace}) {
        show_trace(qq[rpc_maker: @_]);
    }
    my $method = shift;
    sub {
        push @_, $method;
        goto &do_rpc;  # Knock the stub out of the call stack.
    }
}

# AUTOLOAD installs RPC proxies for all unknown methods.
sub AUTOLOAD {
    if ($Opt{trace}) {
        show_trace(qq[AUTOLOAD=$AUTOLOAD, @_]);
    }
    my ($method) = ($AUTOLOAD =~ /::(\w+)$/);
    return if $method eq 'DESTROY';
    my $rpc = rpc_maker($method);
    {
        # Install the RPC proxy method, we will not came here
        # any more for the same method name.
        no strict 'refs';
        *$method = $rpc;
    }
    goto &$rpc;  # Call the RPC now.
}

sub DESTROY {
    $_[0]->_close();
}

# This BEGIN block either invokes server() or sends a client request,
# or does nothing (the case of using Android.pm as a client library).
sub BEGIN {
    if (defined $Opt{server}) {
        &server;
    } elsif (defined $Opt{request}) {
        my $android = Android->new();
        $android->trace(1) if $Opt{trace};
        my $method = shift @ARGV;
        $android->$method(@ARGV);
        exit(0);
    }
}

1;
