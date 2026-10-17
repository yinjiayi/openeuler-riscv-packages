#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
actual_version=$(rpm -q --qf '%{VERSION}' perl-Getopt-Long-Descriptive)
test "$actual_version" = '0.117'
provides=$(rpm -q --provides perl-Getopt-Long-Descriptive)
for cap in 'perl(Getopt::Long::Descriptive) = 0.117' 'perl(Getopt::Long::Descriptive::Opts) = 0.117' 'perl(Getopt::Long::Descriptive::Usage) = 0.117'; do
  grep -Fx "$cap" <<<"$provides"
done
timeout --kill-after=10s 30s perl -MGetopt::Long::Descriptive -MGetopt::Long::Descriptive::Opts -MGetopt::Long::Descriptive::Usage -MDigest::SHA=sha256_hex <<'SMOKE_EOF'
use strict;
use warnings;
delete $ENV{GETOPT_LONG_DESCRIPTIVE_COMPLETION};
delete $ENV{GETOPT_LONG_DESCRIPTIVE_COMPLETION_NAME};
for my $m (qw(Getopt::Long::Descriptive Getopt::Long::Descriptive::Opts Getopt::Long::Descriptive::Usage)) {
 $m->VERSION('0.117'); die "module version $m" unless $m->VERSION eq '0.117';
}
{
 local @ARGV=('--no-enabled','--name','chosen','operand');
 my ($o,$u)=describe_options('smoke %o',['name=s','name option',{default=>'fallback'}],['enabled!','enable option',{default=>1}]);
 die 'default/negatable' unless $o->name eq 'chosen' && $o->enabled==0;
 die 'leftover operand' unless @ARGV==1 && $ARGV[0] eq 'operand';
 my $text=$u->text; die 'usage' unless $text =~ /smoke/ && $text =~ /--name STR/ && $text =~ /--\[no-\]enabled/;
 die 'usage ordering' unless index($text,'name option')<index($text,'enable option');
}
{
 local @ARGV; my ($o)=describe_options('smoke %o',['name=s','name option',{default=>'fallback'}]);
 die 'default' unless $o->name eq 'fallback';
 my $error; {local $@; eval {describe_options('smoke %o',['needed=s','required option',{required=>1}])}; $error=$@;}
 die 'required negative' unless $error =~ /mandatory parameter/i;
}
{
 local @ARGV=('--help');
 my ($o)=describe_options('smoke %o',['needed=s','required option',{required=>1}],['help','help option',{shortcircuit=>1}]);
 die 'shortcircuit' unless $o->help==1 && scalar(keys(%$o))==1;
}
{
 local @ARGV=('operand','--name','later');
 my ($o)=describe_options('smoke %o',['name=s','name option',{default=>'fallback'}],{getopt_conf=>['require_order']});
 die 'require_order' unless $o->name eq 'fallback' && join(' ',@ARGV) eq 'operand --name later';
}
{
 my @spec=(['foo','foo option'],[],['text only'],['bar=s','bar option',{completion=>['a','b']}]);
 my $b=Getopt::Long::Descriptive::_completion_for_bash(@spec);
 die 'bash completion data' unless $b->{flags} eq '--foo --bar' && @{$b->{prev_cases}}==1 && $b->{prev_cases}[0]{action} =~ /a b/;
 my @z=Getopt::Long::Descriptive::_completion_for_zsh(@spec);
 die 'zsh completion data' unless @z==2 && $z[0] =~ /--foo/ && $z[1] =~ /--bar/ && $z[1] =~ /a b/;
}
my $license_root="/usr/share/licenses/perl-Getopt-Long-Descriptive";
my @hashes=(
 ["$license_root/LICENSE","6a6655b220b72111f386ed9a10f11714b2a04f533ecae9655fc192a47a782340"],
 ["$license_root/README","3c6f990efa8a59072e4414ddfd7d1327daeaace6e7f984524164c486bc8404b9"],
 ["$license_root/Changes","732de9ebe73679652fb040d2d362880d41f7c419bb4a1d9cacd4ecbb0c46fb73"],
 ["$license_root/Descriptive.pm","d49319fc19818c3bbb3105c9676e9d104193948ec2fb6fd68ce28d8838b3758c"],
 ["$license_root/Opts.pm","56f3f8b185e7e3d900739035af9e5bb06002a07b54481d5c7d6c614075b593e0"],
 ["$license_root/Usage.pm","06228a87d540d307ffb70443c141d88643501ed37b71691ba932ecc83e1ec67c"],
 ["$license_root/packaging-notices/report-prereqs-0.029-LICENSE.txt","be3dd240eaa427092a00d91655f56e2f49eb73c543eafc6ab1b65a8e6e6ae94d"],
 ["$license_root/packaging-notices/report-prereqs-0.029-README.txt","84cc2aa5dcce178c2618df4dd265837a8df22ddcf584325c72c26181122e947f"],
 ["$license_root/packaging-notices/changes-0.011-LICENSE.txt","b9edff2945afbd8a4482d6d09ed49fe64f65be61d355feeb7328ab53487cd5b4"],
 ["$license_root/packaging-notices/changes-0.011-README.txt","f75ccf813c752850aa21aabff3dced2b53792b0657b387e0f47cb341629728ea"],
 ["$license_root/packaging-notices/version-0.9909-README.txt","2281261147b4fc710bd1920d48e78aa44bc181306dba919ad98cb121a0c8ad21"],
 ["$license_root/packaging-notices/historical-perl-Copying.txt","d77d235e41d54594865151f4751e835c5a82322b0e87ace266567c3391a4b912"],
 ["$license_root/packaging-notices/historical-perl-Artistic.txt","8e6beb9ca0ffbc4b9c6550d56f622ecd33d5635ee8af9a8f269fd81f40fb6801"],
 ["$license_root/packaging-notices/checkbreaks-0.020-LICENCE.txt","6f8e00a769896f6c4091c8a97664497e4efed491f1af8729a3c767acd079b6cb"],
 ["$license_root/packaging-notices/checkbreaks-0.020-README.txt","dc5d7e39c47390b4844f41301acad6fd65b3b6b2afbe7edca43d78fca601dd5a"],
 ["$license_root/packaging-notices/compile-2.059-LICENCE.txt","de32f9928e097dc201258a53ab3c3f003b555ae886fb19e9f4c165923ed5e45f"],
 ["$license_root/packaging-notices/compile-2.059-README.txt","c985bcc4e0eb88ea427b14e19047d5c6320073aae1c736f712bb96bb39d297d8"],
 ["$license_root/packaging-notices/PACKAGING-NOTICE.txt","145d76545ac689b22a12eaaf9448e49aa30cb21b70ffc0a166b286559e35b59c"],
);
for my $r (@hashes) {open my $f,"<",$r->[0] or die $!; binmode $f; my $bytes=do {local $/; <$f>}; close $f or die $!; die "notice hash $r->[0]" unless sha256_hex($bytes) eq $r->[1];}
 {my $p=$INC{"Getopt/Long/Descriptive.pm"}; die "module path" unless defined $p; open my $f,"<",$p or die $!; binmode $f; my $bytes=do {local $/; <$f>}; close $f or die $!; die "module bytes" unless sha256_hex($bytes) eq "d49319fc19818c3bbb3105c9676e9d104193948ec2fb6fd68ce28d8838b3758c";}
 {my $p=$INC{"Getopt/Long/Descriptive/Opts.pm"}; die "module path" unless defined $p; open my $f,"<",$p or die $!; binmode $f; my $bytes=do {local $/; <$f>}; close $f or die $!; die "module bytes" unless sha256_hex($bytes) eq "56f3f8b185e7e3d900739035af9e5bb06002a07b54481d5c7d6c614075b593e0";}
 {my $p=$INC{"Getopt/Long/Descriptive/Usage.pm"}; die "module path" unless defined $p; open my $f,"<",$p or die $!; binmode $f; my $bytes=do {local $/; <$f>}; close $f or die $!; die "module bytes" unless sha256_hex($bytes) eq "06228a87d540d307ffb70443c141d88643501ed37b71691ba932ecc83e1ec67c";}
print "Getopt installed option semantics, completion strings and original byte hashes passed\n";
SMOKE_EOF
