#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-RewritePrefix
rpm -q --whatprovides 'perl(String::RewritePrefix)'
perl -MString::RewritePrefix -e '
  die "unexpected version\n" unless $String::RewritePrefix::VERSION eq "0.009";
  my @got = String::RewritePrefix->rewrite(
    { "" => "App::", "+" => "", "++" => "Vendor::" },
    "Plugin", "+Mixin", "++Addon"
  );
  die "prefix rewrite mismatch\n"
    unless join(",", @got) eq "App::Plugin,Mixin,Vendor::Addon";
'
