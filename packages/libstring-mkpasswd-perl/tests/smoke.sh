#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-MkPasswd
rpm -q --whatprovides 'perl(String::MkPasswd)'
command -v mkpasswd.pl
perl -c "$(command -v mkpasswd.pl)"
perl -MString::MkPasswd -e '
  die "unexpected version\n" unless $String::MkPasswd::VERSION eq "0.05";
  my $value = String::MkPasswd::mkpasswd(-length => 12,
      -minnum => 2, -minlower => 5, -minupper => 3, -minspecial => 2);
  die "generator returned no value\n" unless defined $value;
  my $digits = () = $value =~ /[0-9]/g;
  my $lower = () = $value =~ /[a-z]/g;
  my $upper = () = $value =~ /[A-Z]/g;
  die "length or character class mismatch\n"
    unless length($value) == 12
       && $digits == 2 && $lower == 5 && $upper == 3;
  die "impossible request should fail\n"
    if defined String::MkPasswd::mkpasswd(-length => 1);
'
