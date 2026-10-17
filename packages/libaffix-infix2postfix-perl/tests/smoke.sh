#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
# Installed-only: no source-tree include path or PERL5LIB shortcut.
unset PERL5LIB PERLLIB
rpm -q -- perl-Affix-Infix2Postfix
rpm -q --whatprovides 'perl(Affix::Infix2Postfix)'
perl -MAffix::Infix2Postfix -e '
  die "unexpected installed version\n" unless $Affix::Infix2Postfix::VERSION eq "0.03";
  my $parser = Affix::Infix2Postfix->new(
    ops => [
      {op => "<<"}, {op => ">>"}, {op => "+"}, {op => "-"},
      {op => "*"}, {op => "/"}, {op => "-", type => "unary", trans => "u-"},
      {op => "**"}, {op => "func", type => "unary"}
    ],
    grouping => ["(", ")"], func => ["sin", "cos", "exp", "log"],
    vars => ["x", "y", "z"]
  );
  for my $case (
    ["x+y*z", "x y z * +"],
    ["(x+y)*z", "x y + z *"],
    ["x**y<<2+z", "x y ** 2 z + <<"],
    ["sin(x)+y", "x sin y +"],
    ["-x", "x u-"]
  ) {
    my @actual = $parser->translate($case->[0]);
    die "translation mismatch for $case->[0]\n"
      unless join(" ", @actual) eq $case->[1];
  }
  my $invalid = $parser->translate(q{x@z});
  die "invalid token was not rejected\n" if defined $invalid;
  die "missing invalid token diagnostic\n" unless $parser->{ERRSTR} =~ /^Bad tokens: /;
'

module_path=$(perl -MAffix::Infix2Postfix -e 'print $INC{"Affix/Infix2Postfix.pm"}')
test -f "$module_path"
printf '%s  %s\n' \
  a6a5fb15f86ebd0c051298314c97aa99790907b129c24f6a6f370d1c25662c8a "$module_path" | sha256sum -c -
license_dir=/usr/share/licenses/perl-Affix-Infix2Postfix
printf '%s  %s\n' \
  f2c2b1f929f8e924abae73ae71b817f5143a03d29c07aef7f883499b7ac6140e "$license_dir/README" \
  dd90d4f42e4dcadf5a7c09eea0189d93c7b37ae560c91f0f6d5233ed3b9292a2 "$license_dir/Artistic" \
  d77d235e41d54594865151f4751e835c5a82322b0e87ace266567c3391a4b912 "$license_dir/Copying" | sha256sum -c -
