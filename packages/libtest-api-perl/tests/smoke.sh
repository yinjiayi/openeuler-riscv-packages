#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MTest::More -MTest::API -e '
    BEGIN {
        package EvidenceFixture;
        sub ping { 42 }
        $INC{"EvidenceFixture.pm"} = __FILE__;
    }
    public_ok("EvidenceFixture", "ping");
    done_testing();
'
