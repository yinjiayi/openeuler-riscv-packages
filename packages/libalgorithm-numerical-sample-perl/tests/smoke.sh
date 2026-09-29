#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Algorithm-Numerical-Sample
perl -MAlgorithm::Numerical::Sample=sample -e '
  die "unexpected version\n"
    unless $Algorithm::Numerical::Sample::VERSION eq "2010011201";
  my @all = sample(set => [1 .. 5], sample_size => 5);
  die "full-size sample mismatch\n" unless join(",", @all) eq "1,2,3,4,5";
  my @subset = sample(set => [1 .. 10], sample_size => 3);
  die "subset size mismatch\n" unless @subset == 3;
  my %seen;
  for my $value (@subset) {
    die "subset out of range\n" unless $value >= 1 && $value <= 10;
    die "duplicate subset value\n" if $seen{$value}++;
  }
  my $stream = Algorithm::Numerical::Sample::Stream->new(sample_size => 2);
  $stream->data(1 .. 4);
  my @stream_sample = $stream->extract;
  die "stream sample size mismatch\n" unless @stream_sample == 2;
  %seen = ();
  for my $value (@stream_sample) {
    die "stream value out of range\n" unless $value >= 1 && $value <= 4;
    die "duplicate stream value\n" if $seen{$value}++;
  }
'
