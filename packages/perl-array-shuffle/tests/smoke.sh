#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Array-Shuffle
perl -MArray::Shuffle=shuffle_array,shuffle_huge_array -e 'my @a = (1..5); shuffle_array @a; die "shuffle" unless join(q{,}, sort { $a <=> $b } @a) eq q{1,2,3,4,5}; shuffle_huge_array @a; die "huge shuffle" unless join(q{,}, sort { $a <=> $b } @a) eq q{1,2,3,4,5}'
