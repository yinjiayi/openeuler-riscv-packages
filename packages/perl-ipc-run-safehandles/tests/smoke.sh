#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-ipc-run-safehandles
perl -e '
    use strict;
    use warnings;
    use IPC::Run3 qw(run3);
    use IPC::Run::SafeHandles;
    die "wrong version" unless $IPC::Run::SafeHandles::VERSION eq "0.04";
    my $wrapped = \&IPC::Run3::run3;
    for my $role (q(), q(RESPONDER)) {
        local $ENV{FCGI_ROLE} = $role;
        my ($out, $err) = (q(), q());
        run3([$^X, q(-e), q(print qq(safe-output); warn qq(safe-error\n))], undef, \$out, \$err);
        die "child status" if $?;
        die "stdout capture" unless $out eq q(safe-output);
        die "stderr capture" unless $err eq qq(safe-error\n);
    }
    IPC::Run::SafeHandles->unimport;
    die "wrapper not restored" if \&IPC::Run3::run3 == $wrapped;
'
