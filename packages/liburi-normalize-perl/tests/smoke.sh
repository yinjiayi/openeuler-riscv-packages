#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-URI-Normalize
rpm -q --whatprovides 'perl(URI::Normalize)'
perl -MURI::Normalize=normalize_uri,remove_dot_segments -e '
  die "wrong URI::Normalize version\n"
    unless $URI::Normalize::VERSION eq "0.002";
  die "URI normalization failed\n"
    unless normalize_uri("HTTPS://www.example.com:443/../test/../foo/index.html")
      eq "https://www.example.com/foo/index.html";
  die "dot-segment removal failed\n"
    unless remove_dot_segments("https://www.example.com/foo/../bar")
      eq "https://www.example.com/bar";
'
