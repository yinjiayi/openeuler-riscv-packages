#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
if [ "$(id -u)" = 0 ]; then
    exec /usr/bin/setpriv --reuid=10001 --regid=10001 --clear-groups --no-new-privs /bin/bash "$0"
fi
test "$(id -u)" = 10001
test "$(id -g)" = 10001
if [ -n "${PERL5OPT-}" ] || [ -n "${PERL5LIB-}" ] || [ -n "${PERLLIB-}" ] || \
   [ -n "${HARNESS_PERL-}" ] || [ -n "${HARNESS_PERL_SWITCHES-}" ] || \
   [ -n "${HARNESS_OPTIONS-}" ] || [ -n "${HARNESS_SUBCLASS-}" ] || \
   [ -n "${HARNESS_IGNORE_EXIT-}" ]; then
    echo 'Refusing Perl/Harness environment overrides in installed smoke' >&2
    exit 1
fi
perl -MCwd::Guard=cwd_guard -MCwd=getcwd,abs_path -MFile::Temp -MDigest::SHA -e '
use strict; use warnings;
die "UID mismatch" unless $< == 10001 && $> == 10001;
for my $group ("$(", "$)") {
  my @ids=split /\s+/, $group;
  die "group mismatch" unless @ids && !grep { $_ != 10001 } @ids;
}
print "SMOKE UID=$< EUID=$> GID=$( EGID=$)\n";
die "version mismatch" unless $Cwd::Guard::VERSION eq "0.05";
die "original fchdir feature unavailable" unless Cwd::Guard::USE_FCHDIR;
sub hashfile {
  my ($path)=@_;
  open my $fh,"<",$path or die "$path: $!";
  binmode $fh;
  return Digest::SHA->new(256)->addfile($fh)->hexdigest;
}
my $module=$INC{"Cwd/Guard.pm"};
die "installed module mismatch" unless hashfile($module) eq "19e5a0f0fb029ec3e815d6270d08bb572d17aefb2f61bbb925e5e0f6aa8bed4d";
my $license="/usr/share/licenses/perl-Cwd-Guard";
for my $item (
  ["LICENSE","226699536be39a2793a964d189438ad406b85bea58aa8afd566ea86b0b9442a9"],
  ["README.md","9931f4893ab08b7ddbef4f5ddde0120b8f13d389c6bb3d802ccdf3117f16c281"],
  ["Changes","a19aa60c57bd75f21cbc9d616c37a9e66a376a1971ad4057fd5498aa147fda3b"],
  ["META.json","9ebe433efa224f1a312591285a134129777d98a95742c3e96df3252b8f63871e"],
  ["META.yml","8f179b57459af4fb27d6002f9205a4fed4f2a57cbd4ca0dbe98d84312f44aa0c"],
  ["Guard.pm","19e5a0f0fb029ec3e815d6270d08bb572d17aefb2f61bbb925e5e0f6aa8bed4d"]
) {
  die "notice mismatch $item->[0]" unless hashfile("$license/$item->[0]") eq $item->[1];
  print "NOTICE $item->[0] SHA256 OK\n";
}
my $start=getcwd();
my $private=File::Temp::tempdir("cwd-guard-smoke-XXXXXXXX",TMPDIR=>1,CLEANUP=>1);
chmod 0700,$private or die "private directory mode: $!";
my @private_stat=stat($private);
die "private directory identity" unless @private_stat && $private_stat[4]==10001 && ($private_stat[2]&0777)==0700;
my $root=abs_path($private);
my $old="$root/original"; my $renamed="$root/renamed"; my $other="$root/other";
mkdir $old,0700 or die $!;
mkdir $other,0700 or die $!;
{
  my $guard=cwd_guard($old) or die "initial chdir: $Cwd::Guard::Error";
  die "scope notentered" unless getcwd() eq $old;
  {
    my $nested=cwd_guard($other) or die "nested chdir: $Cwd::Guard::Error";
    die "nested scope notentered" unless getcwd() eq $other;
  }
  die "nested scope notrestored" unless getcwd() eq $old;
}
die "scope notrestored" unless getcwd() eq $start;
chdir $old or die $!;
my @before=stat(".");
{
  my $guard=Cwd::Guard->new($root) or die "rename guard: $Cwd::Guard::Error";
  rename $old,$renamed or die "rename: $!";
  die "guard directory changed" unless getcwd() eq $root;
}
my @after=stat(".");
die "renamed inode restoration" unless @before && @after && $before[0]==$after[0] && $before[1]==$after[1] && getcwd() eq $renamed;
chdir $start or die $!;
my $failure=cwd_guard("$root/nonexistent");
die "missing directory accepted" if defined $failure;
die "missing Error semantics" unless $Cwd::Guard::Error;
die "failed chdir moved cwd" unless getcwd() eq $start;
print "Cwd::Guard0.05 private scope/nested/renamed-inode/undefined-error semantics PASS\n";
'
rpm -q --provides perl-Cwd-Guard | grep -Fx 'perl(Cwd::Guard) = 0.05'
