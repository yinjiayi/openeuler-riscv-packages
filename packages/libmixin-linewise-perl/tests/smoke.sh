#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
rpm -q perl-Mixin-Linewise
for capability in 'perl(Mixin::Linewise) = 0.111' 'perl(Mixin::Linewise::Readers) = 0.111' 'perl(Mixin::Linewise::Writers) = 0.111'; do
  rpm -q --provides perl-Mixin-Linewise | grep -Fx "$capability"
done
timeout 120 perl <<'PERL'
use strict;
use warnings;
use utf8;
use Encode qw(encode encode_utf8);
use Digest::SHA qw(sha256_hex);
use File::Temp qw(tempdir);
use Mixin::Linewise::Readers ();
use Mixin::Linewise::Writers ();
die "Readers version" unless $Mixin::Linewise::Readers::VERSION eq '0.111';
die "Writers version" unless $Mixin::Linewise::Writers::VERSION eq '0.111';
{
  package InstalledReader;
  use Mixin::Linewise::Readers -readers,
    -readers => { -suffix => '_alternate', method => 'read_alt_handle' };
  sub read_handle { my ($self,$handle)=@_; local $/; return scalar <$handle>; }
  sub read_alt_handle { my ($self,$handle)=@_; return 'alternate:'.$self->read_handle($handle); }
}
{
  package InstalledRawReader;
  use Mixin::Linewise::Readers -readers => { binmode => 'raw' };
  sub read_handle { my ($self,$handle)=@_; local $/; return scalar <$handle>; }
}
{
  package InstalledWriter;
  use Mixin::Linewise::Writers -writers;
  sub write_handle { my ($self,$data,$handle)=@_; print {$handle} $data or die "write: $!"; }
}
sub equal { my($got,$want,$name)=@_; die "$name mismatch" unless defined($got) && $got eq $want; }
my $dir=tempdir('mixin-linewise-smoke-XXXXXXXX',TMPDIR=>1,CLEANUP=>1);
my $file="$dir/input";
my $text="author = ®icardo Sígnes\n";
my $bytes=encode_utf8($text);
equal(InstalledReader->read_string($bytes),$text,'UTF8 string reader');
equal(InstalledReader->read_string_alternate($bytes),'alternate:'.$text,'custom read method');
equal(InstalledRawReader->read_string($bytes),$bytes,'raw string reader');
equal(InstalledWriter->write_string($text),$bytes,'UTF8 string writer');
InstalledWriter->write_file($text,$file);
equal(InstalledReader->read_file($file),$text,'UTF8 file reader/writer');
equal(InstalledRawReader->read_file($file),$bytes,'raw file reader');
equal(InstalledReader->read_file({binmode=>'raw'},$file),$bytes,'raw file override');
my $latin="Ĉamomile\n";
my $latinbytes=encode('Latin-3',$latin);
equal(InstalledWriter->write_string({binmode=>'encoding(Latin-3)'},$latin),$latinbytes,'Latin3 writer');
equal(InstalledReader->read_string({binmode=>'encoding(Latin-3)'},$latinbytes),$latin,'Latin3 reader');
InstalledWriter->write_file($latin,{binmode=>'encoding(Latin-3)'},$file);
equal(InstalledReader->read_file({binmode=>'encoding(Latin-3)'},$file),$latin,'Latin3 file roundtrip');
equal(InstalledWriter->write_string({binmode=>'raw'},$bytes),$bytes,'raw string writer');
for my $case ([sub {InstalledReader->read_string(undef)},qr/no string provided/], [sub {InstalledReader->read_file()},qr/no filename specified/], [sub {InstalledReader->read_file("$dir/absent")},qr/does not exist/], [sub {InstalledReader->read_file($dir)},qr/is not readable/], [sub {InstalledWriter->write_file('x',$dir)},qr/is not a plain file/], [sub {InstalledWriter->write_file('x','')},qr/no filename specified/]) {
  my($call,$pattern)=@$case;
  eval {$call->()}; die "invalid input accepted/wrong failure" unless $@ =~ $pattern;
}
my $top=$INC{'Mixin/Linewise/Readers.pm'};
$top =~ s{/Linewise/Readers[.]pm$}{/Linewise.pm} or die "module path";
my %hashes=(
  $top=>'6598039806d5b9f85636cb4b5d18381bd8f81e994e361717ee12bc0364eb9db5',
  $INC{'Mixin/Linewise/Readers.pm'}=>'703548bf876287d0855d3115bd2a3c551917df5870443e6f65e1a84e39a38b28',
  $INC{'Mixin/Linewise/Writers.pm'}=>'dcad5b3f178b86d5f8411584a187bf17bb2f0de550702affae21fede40527706',
  '/usr/share/licenses/perl-Mixin-Linewise/LICENSE'=>'aa5c9ccb79645771a354fec95fbe77bd11f3351606cd7fc1152edfe9eeedba5a',
  '/usr/share/licenses/perl-Mixin-Linewise/README'=>'af80164c05ca42c2823a1b0569d4c3593e622f28d81fe49933a691097176f953',
  '/usr/share/licenses/perl-Mixin-Linewise/Changes'=>'e212d1a0b4e342bd517ea327310d328268075b645db40370c38bfcc08d48edfc',
);
for my $path (sort keys %hashes) { open my $fh,'<',$path or die "$path: $!"; binmode $fh; local $/; die "source/notice hash $path" unless sha256_hex(<$fh>) eq $hashes{$path}; print "Original source/notice hash OK: $path\n"; }
print "Mixin::Linewise0.111 installed reader/writer semantics verified\n";
PERL
