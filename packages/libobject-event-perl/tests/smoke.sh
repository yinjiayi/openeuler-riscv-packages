#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-object-event
perl -MObject::Event -e '
    die "unexpected Object::Event version\n" unless $Object::Event::VERSION eq "1.23";
    my $event = Object::Event->new;
    my $received = 0;
    my $guard = $event->reg_cb(example => sub { $received += $_[1] });
    $event->event(example => 7);
    die "registered callback did not receive the payload\n" unless $received == 7;
    print "ok - installed event dispatch invokes registered callback\n";
'
