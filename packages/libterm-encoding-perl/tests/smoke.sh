#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-term-encoding
perl -MI18N::Langinfo -MTerm::Encoding=term_encoding -e '
    die "unexpected module version" unless $Term::Encoding::VERSION eq "0.03";
    my $expected = I18N::Langinfo::langinfo(I18N::Langinfo::CODESET());
    die "native encoding lookup failed" unless length($expected) && term_encoding() eq lc($expected);
    no warnings "redefine", "prototype";
    local *I18N::Langinfo::langinfo = sub { undef };
    local $ENV{LANGUAGE} = "ja_JP.euc";
    die "encoding fallback failed" unless term_encoding() eq "euc-jp";
    print "installed Term::Encoding native and locale fallback passed\n";
'
