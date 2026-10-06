#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
rpm -q perl-App-Options
test "$(rpm -q --qf '%{VERSION}\n' perl-App-Options)" = 1.12
rpm -q --provides perl-App-Options | grep -Fx 'perl(App::Options) = 1.12'
test -x /usr/bin/prefix
test -x /usr/bin/prefixadmin
bash -n /usr/bin/prefix
timeout --kill-after=10s 60s perl <<'PERL'
use strict;
use warnings;
use App::Options ();
use Date::Format ();
use File::Find ();
use Fcntl ();
use File::Temp qw(tempdir);
use Digest::SHA qw(sha256_hex);
die "module version" unless $App::Options::VERSION eq '1.12';
print "1..3\n";
my %hashes=(
 $INC{'App/Options.pm'}=>'4bd0d42972f05c0d0daf365fde041637b89c75ccaf00247f4230885b6489c50d',
 '/usr/share/licenses/perl-App-Options/Options.pm'=>'4bd0d42972f05c0d0daf365fde041637b89c75ccaf00247f4230885b6489c50d',
 '/usr/share/licenses/perl-App-Options/perl538-Copying'=>'d77d235e41d54594865151f4751e835c5a82322b0e87ace266567c3391a4b912',
 '/usr/share/licenses/perl-App-Options/perl538-Artistic'=>'dd90d4f42e4dcadf5a7c09eea0189d93c7b37ae560c91f0f6d5233ed3b9292a2',
);
for my $p (sort keys %hashes) {
 open my $fh,'<',$p or die "$p: $!"; binmode $fh; local $/;
 die "original module/notice hash: $p" unless sha256_hex(<$fh>) eq $hashes{$p};
 print "# Original module/notice hash OK: $p\n";
}
my %programs=(
 '/usr/bin/prefix'=>['#!/bin/bash','a958b2e999d785c0be9a5750bc1838f602b81706472ee11519008dfc6305ae6f'],
 '/usr/bin/prefixadmin'=>['#!/usr/bin/perl -w','482bd967d85f3a8d26cd82d8aa2b244b71df40d5f0d2a87834e365d86fa9be95'],
);
for my $p (sort keys %programs) {
 open my $fh,'<',$p or die "$p: $!"; binmode $fh;
 my $first=<$fh>; chomp $first;
 die "intended program interpreter: $p" unless $first eq $programs{$p}[0];
 local $/; die "unchanged installed program body: $p" unless sha256_hex(<$fh>) eq $programs{$p}[1];
 print "# Original CLI body and intended interpreter OK: $p\n";
}
print "ok 1 - original version/provider/module/notice bytes and retained CLI dependencies\n";
my $dir=tempdir('app-options-smoke-XXXXXXXX',TMPDIR=>1,CLEANUP=>1);
die "unsafe private fixture path" unless $dir =~ m{\A/[A-Za-z0-9_./-]+\z};
local @ARGV;
my $obj=App::Options->new({no_cmd_args=>1,no_env_vars=>1,no_option_file=>1,option=>{greeting=>{default=>'Hello'}}});
die "constructor" unless ref($obj) eq 'App::Options';
my %values=(prefix=>$dir,perlinc=>'');
$obj->read_options(\%values);
die "default/hostname" unless $values{greeting} eq 'Hello' && $values{hostname} && $values{host};
print "ok 2 - actual new/read_options default and hostname API (no obsolete init/:none)\n";
open my $data,'>',"$dir/input.txt" or die "input: $!";
print {$data} "private text\n" or die "input write: $!"; close $data or die "input close: $!";
open my $conf,'>',"$dir/options.conf" or die "conf: $!";
print {$conf} "[app=demo]\nanswer = 42\n[ALL]\nexpanded = \${prefix}/one\nfrom_file = < $dir/input.txt\nfrom_pipe = cat $dir/input.txt |\n" or die "conf write: $!";
close $conf or die "conf close: $!";
my %v=(app=>'demo',prefix=>$dir);
my @paths=("$dir/options.conf");
$obj->read_option_files(\%v,\@paths,$dir,{});
die "private configuration" unless $v{answer} eq '42' && $v{expanded} eq "$dir/one" && $v{from_file} eq "private text\n" && $v{from_pipe} eq "private text\n";
my $bad=App::Options->new({no_cmd_args=>1,no_env_vars=>1,no_option_file=>1,option=>'invalid'});
eval {$bad->read_options({prefix=>$dir,perlinc=>''})};
die "expected option argument rejection" unless $@ =~ /'option' arg must be a hash reference/;
print "ok 3 - private file/conditional/substitution/cat-pipe and invalid option behavior\n";
PERL
