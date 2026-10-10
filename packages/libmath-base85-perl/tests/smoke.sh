#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q perl-Math-Base85
rpm -q --provides perl-Math-Base85 | grep -F 'perl(Math::Base85) = 0.5'
for entry in \
  'LICENSE:92bf21030d1cefa9f5c7660b0f861a93f20e0cbb4da0dfab0d988d8dac9b6a29' \
  'README.md:01ac0f7d38b378d75b5e8dd6c5cbda79d2f5478827544891a28ece09a0399181' \
  'rfc1924.txt:a7a388e155294a60ab16d857dcbb6bb50fa5c954001398d67ae7c8aa2a63229c'; do
  filename=${entry%%:*}
  digest=${entry#*:}
  notice=$(rpm -ql perl-Math-Base85 | awk -v name="$filename" '/\/licenses\// { n=split($0, parts, "/"); if(parts[n]==name) print }')
  test -n "$notice"
  printf '%s  %s\n' "$digest" "$notice" | sha256sum -c -
done
perl -MMath::Base85 -MMath::BigInt -e '
use strict;
use warnings;
die "version" unless $Math::Base85::VERSION eq "0.5";
die "alphabet" unless length($Math::Base85::base85_digits) == 85;
my $zero = Math::BigInt->new(0);
die "zero encode" unless Math::Base85::to_base85($zero) eq "0";
die "zero decode" unless Math::Base85::from_base85("0")->is_zero;
my $number = Math::BigInt->new("21932261930451111902915077091070067066");
my $encoded = "4)+k&C#VzJ4br>0wv%Yp";
die "RFC vector encode" unless Math::Base85::to_base85($number) eq $encoded;
die "RFC vector decode" unless Math::Base85::from_base85($encoded) == $number;
for my $value (1, 84, 85, 255, 65535) {
  my $n = Math::BigInt->new($value);
  my $s = Math::Base85::to_base85($n);
  die "roundtrip $value" unless Math::Base85::from_base85($s) == $n;
}
my $accepted = eval { Math::Base85::from_base85("\""); 1 };
die "invalid digit accepted" if $accepted || $@ !~ /invalid base 85 digit/;
print "Math::Base85 installed semantics OK\n";
'
