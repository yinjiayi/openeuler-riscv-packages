#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
perl -MTest::LongString -MTest::More -e '
  plan tests => 3;
  is_string("alpha\nbeta", "alpha\nbeta", "exact multiline equality");
  contains_string("alpha\nbeta", "beta", "contains a substring");
  lacks_string("alpha\nbeta", "gamma", "lacks an absent substring");
'
