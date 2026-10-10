#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q --qf '%{VERSION}\n' perl-IO-TieCombine | grep -Fx '1.005'
for cap in 'perl(IO::TieCombine) = 1.005' 'perl(IO::TieCombine::Handle) = 1.005' 'perl(IO::TieCombine::Scalar) = 1.005'; do
  rpm -q --provides perl-IO-TieCombine | grep -Fx "$cap"
done
perl -MIO::TieCombine -MIO::TieCombine::Handle -MIO::TieCombine::Scalar -MDigest::SHA=sha256_hex -e '
for my $m (qw(IO::TieCombine IO::TieCombine::Handle IO::TieCombine::Scalar)) { $m->VERSION(1.005); no strict "refs"; die "version" unless ${"${m}::VERSION"} eq "1.005"; }
my $hub=IO::TieCombine->new; my $a=$hub->scalar_ref("a"); my $b=$hub->fh("b"); my $cb=$hub->callback("c");
$$a.="one"; print {$b} "two"; $cb->("three"); die "ordering" unless $hub->combined_contents eq "onetwothree";
die "slots" unless $hub->slot_contents("a") eq "one" && $hub->slot_contents("b") eq "two" && $hub->slot_contents("c") eq "three";
eval {$$a="replace"}; die "negative reassignment" unless $@ =~ /append, not reassign/;
die "negative fileno" unless fileno($b)<0; $hub->clear_slot("a"); die "clear" unless $hub->slot_contents("a") eq "" && $hub->combined_contents eq "onetwothree";
eval {$hub->slot_contents("missing")}; die "missing slot" unless $@;
tie my $direct,$hub,"direct"; $direct.="four"; die "direct tie" unless $hub->slot_contents("direct") eq "four";
 {open my $f,"<","/usr/share/licenses/perl-IO-TieCombine/LICENSE" or die $!; binmode $f; local $/; die "notice hash" unless sha256_hex(<$f>) eq "2fdd2e27a911b2ef249a58d73ac741e2480039df8dce354ea813c8c638aab4d5";}
 {open my $f,"<","/usr/share/licenses/perl-IO-TieCombine/README" or die $!; binmode $f; local $/; die "notice hash" unless sha256_hex(<$f>) eq "b496fde52a5fdda2506b1fca3d59296de063cce9f5f65f1b0a62e234c37421c0";}
 {open my $f,"<","/usr/share/licenses/perl-IO-TieCombine/Changes" or die $!; binmode $f; local $/; die "notice hash" unless sha256_hex(<$f>) eq "26c80698a2651f83dbf6b310f1ef3ed7997b1d7695526fc020030431572e0f8c";}
{ my $path=$INC{"IO/TieCombine.pm"}; die "module path" unless defined $path; {open my $f,"<",$path or die $!; binmode $f; local $/; die "module hash" unless sha256_hex(<$f>) eq "bc73553a978e2cec326e3fcbe184e5ae3e09a4bcb43c0ca7edc6af41d4743ec4";} }
{ my $path=$INC{"IO/TieCombine/Handle.pm"}; die "module path" unless defined $path; {open my $f,"<",$path or die $!; binmode $f; local $/; die "module hash" unless sha256_hex(<$f>) eq "0cb30ade672b38eeea7da098393ce119e1805a088e1c4555ba8d4bc2244a728d";} }
{ my $path=$INC{"IO/TieCombine/Scalar.pm"}; die "module path" unless defined $path; {open my $f,"<",$path or die $!; binmode $f; local $/; die "module hash" unless sha256_hex(<$f>) eq "da917ff3ccfe21b34733ffd97dd22398407596e3d4820f981b3abe31471285b4";} }
 {open my $f,"<","/usr/share/licenses/perl-IO-TieCombine/packaging-notices/changes-LICENSE.txt" or die $!; binmode $f; local $/; die "supplement notice hash" unless sha256_hex(<$f>) eq "632db868186eb8245ea6a320775af4b79d495077cf0524fcb9339d5b1375dede";}
 {open my $f,"<","/usr/share/licenses/perl-IO-TieCombine/packaging-notices/changes-README.txt" or die $!; binmode $f; local $/; die "supplement notice hash" unless sha256_hex(<$f>) eq "e83d7f71a2e2620e2cf1c0f281a7f70086640ddceef44602bb06303ec8320d20";}
 {open my $f,"<","/usr/share/licenses/perl-IO-TieCombine/packaging-notices/jerome-LICENSE.txt" or die $!; binmode $f; local $/; die "supplement notice hash" unless sha256_hex(<$f>) eq "0fd88c56cd3e37e30f4072d8cac8c76b80e3be189c7fb74b7d5e6cacf4d9b340";}
 {open my $f,"<","/usr/share/licenses/perl-IO-TieCombine/packaging-notices/jerome-README.txt" or die $!; binmode $f; local $/; die "supplement notice hash" unless sha256_hex(<$f>) eq "74ed6ef9c20f06e7c7ac6e56290e9d87310b28588767cfe46bd08b859595e146";}
 {open my $f,"<","/usr/share/licenses/perl-IO-TieCombine/packaging-notices/reporter-LICENSE.txt" or die $!; binmode $f; local $/; die "supplement notice hash" unless sha256_hex(<$f>) eq "4c5f87ffa218ebe4027858643dad7133fcb8401f842cfaa4f425393fae1ddea2";}
 {open my $f,"<","/usr/share/licenses/perl-IO-TieCombine/packaging-notices/reporter-README.txt" or die $!; binmode $f; local $/; die "supplement notice hash" unless sha256_hex(<$f>) eq "4aefd1fd2fbd04f53e33200815c36a40060bf118a2d77605ca019e8bf39ea541";}
 {open my $f,"<","/usr/share/licenses/perl-IO-TieCombine/packaging-notices/version-Artistic.txt" or die $!; binmode $f; local $/; die "supplement notice hash" unless sha256_hex(<$f>) eq "8e6beb9ca0ffbc4b9c6550d56f622ecd33d5635ee8af9a8f269fd81f40fb6801";}
 {open my $f,"<","/usr/share/licenses/perl-IO-TieCombine/packaging-notices/version-Copying.txt" or die $!; binmode $f; local $/; die "supplement notice hash" unless sha256_hex(<$f>) eq "d77d235e41d54594865151f4751e835c5a82322b0e87ace266567c3391a4b912";}
 {open my $f,"<","/usr/share/licenses/perl-IO-TieCombine/packaging-notices/version-README.txt" or die $!; binmode $f; local $/; die "supplement notice hash" unless sha256_hex(<$f>) eq "2281261147b4fc710bd1920d48e78aa44bc181306dba919ad98cb121a0c8ad21";}
 {open my $f,"<","/usr/share/licenses/perl-IO-TieCombine/packaging-notices/PACKAGING-NOTICE.txt" or die $!; binmode $f; local $/; die "packaging provenance hash" unless sha256_hex(<$f>) eq "dec5dcba668b3de6fddb2019e4d003f78f5b679fdb7cae01db81c71bc58b83c3";}
print "IO::TieCombine installed memory semantics and original byte hashes passed\n";
'
