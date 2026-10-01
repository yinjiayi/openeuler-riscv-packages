#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-MIME-Base32
rpm -q --whatprovides 'perl(MIME::Base32)'
perl -MMIME::Base32=encode_base32,decode_base32,encode_base32hex,decode_base32hex -e '
  die "unexpected version\n" unless $MIME::Base32::VERSION eq "1.303";
  die "Base32 encode mismatch\n" unless encode_base32("foo") eq "MZXW6";
  die "Base32 decode mismatch\n" unless decode_base32("MZXW6") eq "foo";
  die "base32hex encode mismatch\n" unless encode_base32hex("foo") eq "CPNMU";
  die "base32hex decode mismatch\n" unless decode_base32hex("CPNMU") eq "foo";
'
