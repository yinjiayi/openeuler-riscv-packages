#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libxml-filter-buffertext-perl
perl -MXML::Filter::BufferText -e '
    die "version" unless XML::Filter::BufferText->VERSION eq "1.01";
    package Collector;
    sub characters { push @{$_[0]{data}}, $_[1]{Data}; }
    package main;
    my $collector = bless {data => []}, "Collector";
    my $filter = XML::Filter::BufferText->new(Handler => $collector);
    $filter->start_document;
    $filter->characters({Data => "ri"});
    $filter->characters({Data => "scv"});
    $filter->end_document;
    die "buffering" unless @{$collector->{data}} == 1 && $collector->{data}[0] eq "riscv";
    print "installed SAX buffering passed\n";
'
