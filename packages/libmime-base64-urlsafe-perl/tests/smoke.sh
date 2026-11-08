#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-MIME-Base64-URLSafe
rpm -q --whatprovides 'perl(MIME::Base64::URLSafe)'
perl -MMIME::Base64::URLSafe=urlsafe_b64encode,urlsafe_b64decode -e '
  die "unexpected version\n" unless $MIME::Base64::URLSafe::VERSION eq "0.01";
  die "URL-safe alphabet mismatch\n" unless urlsafe_b64encode("\xfb\xff") eq "-_8";
  die "decode mismatch\n" unless urlsafe_b64decode("-_8") eq "\xfb\xff";
  die "padding mismatch\n" unless urlsafe_b64encode("foo") eq "Zm9v";
  die "round-trip mismatch\n" unless urlsafe_b64decode(urlsafe_b64encode("binary\0data")) eq "binary\0data";
'
