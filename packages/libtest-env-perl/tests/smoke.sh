#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MTest::More=tests,1 -MTest::Env -e '
    local $ENV{OPENEULER_TEST_ENV_SMOKE} = "expected value";
    env_ok("OPENEULER_TEST_ENV_SMOKE", "expected value") or exit 1;
'
