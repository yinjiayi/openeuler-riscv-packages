#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export PATH=/usr/bin:/bin
rpm -q perl-Log-Trace
oe_trace_provides=$(rpm -q --provides perl-Log-Trace)
grep -Fx 'perl(Log::Trace) = 1.070' <<<"$oe_trace_provides"
printf '%s\n' \
  '204d8eff92f95aac4df6c8122bc1505f468f3a901e5a4cc08940e0ede1938994  /usr/share/licenses/perl-Log-Trace/COPYING' \
  'edde8369745f59155d5888c8513ccf7c94bdf196d4912db6517a4a7bb3287eae  /usr/share/licenses/perl-Log-Trace/README' \
  '579828d4b3004c26565a6a501e648b4ad48bf5007a54e5c3cbb5b6c9a387de15  /usr/share/licenses/perl-Log-Trace/Trace.pm' \
  '8c3ef7db3e58907b12c97f81ffa800bf51931bf3b1c8ba152cc140f32780492a  /usr/share/licenses/perl-Log-Trace/Manual.pod' \
  '56e32fddd25065fe52784937592d2398e668e59a9cd2f68a0ef99913ec335024  /usr/share/licenses/perl-Log-Trace/Changes' | sha256sum -c -
oe_trace_module=$(/usr/bin/perl -MLog::Trace -e 'print $INC{"Log/Trace.pm"}')
printf '%s  %s\n' '579828d4b3004c26565a6a501e648b4ad48bf5007a54e5c3cbb5b6c9a387de15' "$oe_trace_module" | sha256sum -c -
/usr/bin/timeout 60 /usr/bin/perl <<'PERL'
use strict;
use warnings;
use Log::Trace;
use Data::Dumper;
use Data::Serializer;
use Data::Serializer::Data::Dumper;
die "runtime VERSION" unless $Log::Trace::VERSION eq '1.070';
my $buffer='';
Log::Trace->import(buffer=>\$buffer);
TRACE('alpha','beta');
die "buffer bytes" unless $buffer eq "alpha,beta\n";
$buffer='';
Log::Trace->import(buffer=>\$buffer,{Level=>2});
TRACE({Level=>1},'visible');
TRACE({Level=>3},'hidden');
TRACE('undefined');
die "level filtering" unless $buffer eq "visible\n";
my @custom;
Log::Trace->import(custom=>sub {push @custom, [@_]});
TRACE('callback','value');
die "custom args" unless @custom==1 && @{$custom[0]}==2 && $custom[0][0] eq 'callback' && $custom[0][1] eq 'value';
my $dump='';
Log::Trace->import(custom=>sub {$dump=shift});
DUMP([1,2,3]);
die "DataDumper semantics" unless $dump eq "\$VAR1 = [\n  1,\n  2,\n  3\n];\n";
$dump='';
Log::Trace->import(custom=>sub {$dump=shift},{Dumper=>'Data::Dumper'});
DUMP([1,2,3]);
die "Serializer backend semantics" unless $dump eq "[1,2,3]\n";
$dump='';
my $returned=DUMP([1,2,3]);
die "returned dump traces unexpectedly" unless $dump eq '' && $returned eq "[1,2,3]\n";
print "Log::Trace installed VERSION1.070 buffer/custom/levels/dump semantics OK\n";
PERL
