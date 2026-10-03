#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-TtyLength
rpm -q --whatprovides 'perl(String::TtyLength)'
perl -MUnicode::EastAsianWidth -MString::TtyLength=tty_length,tty_width -e '
  use utf8;
  die "unexpected String::TtyLength version\n"
    unless $String::TtyLength::VERSION eq "0.03";
  die "ANSI length mismatch\n"
    unless tty_length("\e[31mfoo\e[0m") == 3;
  die "ASCII width mismatch\n" unless tty_width("foo") == 3;
  die "CJK width mismatch\n" unless tty_width("こんにちは") == 10;
  die "emoji width mismatch\n" unless tty_width("😄") == 2;
  die "ANSI CJK width mismatch\n"
    unless tty_width("\e[32mこんにちは\e[0m") == 10;
'
