#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-throwable
perl -e '
    use strict;
    use warnings;
    use Class::Throwable "Local::ThrowableSmoke";
    die "unexpected Class::Throwable version\n" unless $Class::Throwable::VERSION eq "0.13";
    eval { Local::ThrowableSmoke->throw("expected exception") };
    my $error = $@;
    die "unexpected exception class\n" unless ref($error) eq "Local::ThrowableSmoke";
    die "unexpected exception message\n" unless $error->getMessage eq "expected exception";
    print "ok - installed throwable preserves exception class and message\n";
'
