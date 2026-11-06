#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-MIME-EncWords
rpm -q --whatprovides 'perl(MIME::EncWords)'
rpm -q --whatprovides 'perl(Encode::MIME::EncWords)'
perl -MEncode -MEncode::MIME::EncWords -MMIME::EncWords=:all -e '
  die "unexpected MIME::EncWords version\n" unless $MIME::EncWords::VERSION eq "1.015.0";
  die "encoded header decode mismatch\n"
    unless Encode::decode("MIME-EncWords", "=?UTF-8?B?4piD?=") eq "\x{2603}";
  die "plain ASCII mismatch\n" unless encode_mimewords("plain ASCII") eq "plain ASCII";
'
