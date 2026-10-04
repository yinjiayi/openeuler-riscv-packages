#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
rpm -q perl-Number-Format
rpm -q --provides perl-Number-Format | grep -Fx 'perl(Number::Format) = 1.79'
timeout 120 perl <<'PERL'
use strict;
use warnings;
use POSIX qw(setlocale LC_ALL);
use Digest::SHA qw(sha256_hex);
use Number::Format qw(round);
die "C locale" unless defined setlocale(LC_ALL, 'C');
die "module version" unless $Number::Format::VERSION eq '1.79';
sub equal { my ($actual,$expected,$name)=@_; die "$name: unexpected value" unless defined($actual) && $actual eq $expected; }
equal(round(1.005,2), '1.01','rounding');
my $n=Number::Format->new(thousands_sep=>',',decimal_point=>'.',decimal_fill=>1,decimal_digits=>2,neg_format=>'(x)',mon_thousands_sep=>',',mon_decimal_point=>'.',int_curr_symbol=>'USD',currency_symbol=>'$' ,int_frac_digits=>2,frac_digits=>2,n_cs_precedes=>1,n_sep_by_space=>1,n_sign_posn=>1,negative_sign=>'-',p_cs_precedes=>1,p_sep_by_space=>1,p_sign_posn=>1,positive_sign=>'');
equal($n->format_number(1234567.8),'1,234,567.80','grouping/fill');
equal($n->format_number(-12.5),'(12.50)','negative');
equal($n->format_price(-9.95),'-USD 9.95','monetary sign');
my $picture=Number::Format->new(thousands_sep=>',',decimal_point=>'.',neg_format=>'x');
equal($picture->format_picture(100023,'USD ##,###.##'),'USD **,***.**','picture overflow');
equal($n->format_bytes(2048,mode=>'iec'),'2.00KiB','IEC bytes');
equal($n->format_bytes(2048,mode=>'trad'),'2.00K','traditional bytes');
equal($n->unformat_number('4TiB'),4*2**40,'byte parsing');
equal($n->unformat_number('(1,234.50)'),-1234.5,'negative parsing');
my $de=Number::Format->new(thousands_sep=>'&nbsp;',decimal_point=>',');
equal($de->format_number(12345678.5),'12&nbsp;345&nbsp;678,5','custom separators');
for my $case ([sub {$n->format_bytes(-1)},qr/Negative/], [sub {$n->format_negative(1,'bad')},qr/x/], [sub {$n->unformat_number('4G',base=>0)},qr/positive integer/], [sub {Number::Format->new(unknown_option=>1)},qr/Invalid argument/]) {
  my ($call,$pattern)=@$case; eval {$call->()}; die "invalid input accepted/wrong failure" unless $@ =~ $pattern;
}
my %hashes=(
 $INC{'Number/Format.pm'}=>'e069f3ca8519b384396d75c3382e941c23b55158cc9025491330e97d9bde199a',
 '/usr/share/licenses/perl-Number-Format/LICENSE'=>'11739ffa17f5355f74204ce0e9326a02bb0cac14d90cdb62b7ed5c27cb2c6632',
 '/usr/share/licenses/perl-Number-Format/README'=>'8080b68b787d4a355c65a86091f0af073aef94623e30d5c4fbf62f44e081f9e5',
 '/usr/share/licenses/perl-Number-Format/Changes'=>'155f1a2994290aa464673724854e419203e697897a15205eae883daa22510316',
);
for my $path (sort keys %hashes) { open my $fh,'<',$path or die "$path: $!"; binmode $fh; local $/; die "source/notice hash $path" unless sha256_hex(<$fh>) eq $hashes{$path}; print "Original source/notice hash OK: $path\n"; }
print "Number::Format1.79 installed C-locale semantics verified\n";
PERL
