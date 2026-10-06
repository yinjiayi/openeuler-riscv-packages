#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
if [ "$(id -u)" = 0 ]; then
    exec /usr/bin/setpriv --reuid=10001 --regid=10001 --clear-groups --no-new-privs /bin/bash "$0"
fi
test "$(id -u)" = 10001
test "$(id -g)" = 10001
perl -MApache::Htgroup -MFile::Temp -MDigest::SHA -e '
use strict; use warnings;
die "UID mismatch" unless $< == 10001 && $> == 10001;
for my $g ("$(", "$)") { my @ids=split /\s+/, $g; die "group mismatch" unless @ids && !grep { $_ != 10001 } @ids; }
print "SMOKE UID=$< EUID=$> GID=$( EGID=$)\n";
die "version mismatch" unless $Apache::Htgroup::VERSION eq "1.23";
sub hashfile { my ($p)=@_; open my $fh,"<",$p or die "$p: $!"; binmode $fh; return Digest::SHA->new(256)->addfile($fh)->hexdigest; }
my $module=$INC{"Apache/Htgroup.pm"};
die "installed module mismatch" unless hashfile($module) eq "20b55cb48d13f39b3f0ddfb50d2826ee3e658d00bcd4fc0b57b9a79a22d80cf1";
my $lic="/usr/share/licenses/perl-Apache-Htgroup";
for my $item (["LICENSE","bd1f75e539026ddc5486438237b6d95363725387871d6ac997cd231955fd4fa2"],["README","40263015fb2b7d7ddcf7d09c799d743e2b302b5f7bade0e8d7fad34f43b32c25"],["Htgroup.pm","20b55cb48d13f39b3f0ddfb50d2826ee3e658d00bcd4fc0b57b9a79a22d80cf1"]) {
 die "notice mismatch $item->[0]" unless hashfile("$lic/$item->[0]") eq $item->[1];
 print "NOTICE $item->[0] SHA256 OK\n";
}
my $dir=File::Temp::tempdir("htgroup-smoke-XXXXXXXX", TMPDIR=>1, CLEANUP=>1);
my $path="$dir/groups";
my $obj=Apache::Htgroup->new;
die "new notempty" if keys %{$obj->groups};
$obj->adduser("alice","admins"); $obj->adduser("bob","admins");
die "membership" unless $obj->ismember("alice","admins") && $obj->ismember("bob","admins");
$obj->deleteuser("bob","admins"); die "deleteuser" if $obj->ismember("bob","admins");
$obj->adduser("guest","temporary"); $obj->deletegroup("temporary");
die "deletegroup" if exists $obj->groups->{temporary};
$obj->adduser("last","empty"); $obj->deleteuser("last","empty");
die "save" unless $obj->save($path);
my $loaded=Apache::Htgroup->load($path);
die "persistence" unless $loaded->ismember("alice","admins") && !$loaded->ismember("bob","admins") && !exists($loaded->groups->{temporary});
die "emptygroup" unless exists($loaded->groups->{empty}) && !keys %{$loaded->groups->{empty}};
$loaded->adduser("carol","admins"); $loaded->save; $loaded->reload;
die "reload saved" unless $loaded->ismember("alice","admins") && $loaded->ismember("carol","admins");
my $ok=eval { Apache::Htgroup->load("$dir/missing"); 1 };
die "missing error notpropagated" if $ok || !$@;
print "Apache::Htgroup1.23 private groupfile semantics PASS\n";
'
rpm -q --provides perl-Apache-Htgroup | grep -Fx 'perl(Apache::Htgroup) = 1.23'
