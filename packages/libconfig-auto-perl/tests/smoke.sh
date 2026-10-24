#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
if [ "$(id -u)" = 0 ]; then
    exec /usr/bin/setpriv --reuid=10001 --regid=10001 --clear-groups --no-new-privs /bin/bash "$0"
fi
test "$(id -u)" = 10001
test "$(id -g)" = 10001
if [ -n "${PERL5OPT-}" ] || [ -n "${PERL5LIB-}" ] || [ -n "${PERLLIB-}" ]; then
    echo 'Refusing Perl environment overrides in installed smoke' >&2
    exit 1
fi
perl -MConfig::Auto -MXML::Simple -MYAML::Any -MConfig::IniFiles -MFile::Temp -MDigest::SHA -e '
use strict; use warnings;
die "unsafe smoke identity" unless $< == 10001 && $> == 10001;
die "version mismatch" unless $Config::Auto::VERSION eq "0.44";
my $private=File::Temp::tempdir("config-auto-smoke-XXXXXXXX",TMPDIR=>1,CLEANUP=>1);
chmod 0700,$private or die $!;
my @st=stat($private);
die "private scope identity" unless @st && $st[4]==10001 && ($st[2]&0777)==0700;
local $ENV{HOME}=$private;
chdir $private or die $!;
sub hashfile { my($p)=@_; open my $fh,"<",$p or die "$p: $!"; binmode $fh; return Digest::SHA->new(256)->addfile($fh)->hexdigest; }
die "installed module bytes changed" unless hashfile($INC{"Config/Auto.pm"}) eq "da6267fed1e57d25835c2d68bc0d1d6853f1f62dbaa6cf926b5195b1f1620505";
my $licenses="/usr/share/licenses/perl-Config-Auto";
for my $item (
 ["README","c828f6b61f96e3d392ab4f365b19ce1cfe726bc1782476f2505fe5a4460c3deb"],
 ["Makefile.PL","34b93d9e85d04c2df56e47ffb33888039015fa7314564d0ab0d2c34ebfc84dd2"],
 ["Changes","dd360e3704ad09e2a1a3e8dc87c495673092b0c1ae999f442e38ebab8e5db4fd"],
 ["MANIFEST","9e37bfb2c6628f691d17d12a2e62883efd70353c14eebf3d72cb83be6fb2280e"],
 ["META.json","fb4a6b87569e0063fc9e0485fc3dd5d12f30205887c646636d2d0498f2b5324e"],
 ["META.yml","f355a17f3b771dea3ddbb606ba8ab1089d357310c5dd635d40287cf27e5dcebb"],
 ["Auto.pm","da6267fed1e57d25835c2d68bc0d1d6853f1f62dbaa6cf926b5195b1f1620505"],
 ["App-EUMM-Upgrade-0.21-NOTICE.txt","d08188138c0c49b7a28c573a3d912d42cc7175ebbd9ccc7c090f08ee9ffe7b7b"],
 ["GNU-GPL-3.txt","3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986"],
 ["Perl-Artistic.txt","dd90d4f42e4dcadf5a7c09eea0189d93c7b37ae560c91f0f6d5233ed3b9292a2"],
 ["Perl-Copying.txt","d77d235e41d54594865151f4751e835c5a82322b0e87ace266567c3391a4b912"]
) { die "notice bytes changed $item->[0]" unless hashfile("$licenses/$item->[0]") eq $item->[1]; print "NOTICE $item->[0] SHA256 OK\n"; }
for my $case (
 ["colon","key: value\n", "value"], ["space","key value\n", "value"],
 ["equal","key=value\n", "value"], ["xml","<?xml version=\"1.0\"?><config><key>value</key></config>\n", "value"],
 ["yaml","---\nkey: value\n", "value"]
) {
 my($format,$text,$expected)=@$case;
 my $obj=Config::Auto->new(source=>$text,format=>$format);
 my $parsed=$obj->parse;
 die "parse failed $format" unless ref($parsed) eq "HASH" && $parsed->{key} eq $expected;
}
my $ini=Config::Auto::parse("[group]\nkey=value\n",format=>"ini");
die "INI failed" unless ref($ini) eq "HASH" && $ini->{group}{key} eq "value";
my $list=Config::Auto::parse("one\ntwo\n",format=>"list");
die "list failed" unless ref($list) eq "ARRAY" && join(" ",@$list) eq "one two";
my $code=qq(#!/usr/bin/perl\n{ key => [42, 42] };\n);
my $perl=Config::Auto::parse($code,format=>"perl");
die "original Perl format failed" unless ref($perl) eq "HASH" && join(" ",@{$perl->{key}}) eq "42 42";
{ local $Config::Auto::DisablePerl=1; my $parsed=eval {Config::Auto::parse($code)}; die "DisablePerl ignored" unless !$parsed && $@ =~ /Unparsable file format/; }
for my $format (qw(bind irssi)) {
 my $parsed=eval {Config::Auto::parse("key value\n",format=>$format)};
 die "original unavailable format changed" unless !$parsed && $@ =~ /not supported in this release/;
}
print "Config::Auto0.44 UID10001 private parsing/DisablePerl/original unavailable-format smoke PASS\n";
'
rpm -q --provides perl-Config-Auto | grep -Fx 'perl(Config::Auto) = 0.44'
