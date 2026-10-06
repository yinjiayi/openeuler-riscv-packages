#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
rpm -q perl-App-Control
test "$(rpm -q --qf '%{VERSION}\n' perl-App-Control)" = 1.07
rpm -q --provides perl-App-Control | grep -Fx 'perl(App::Control) = 1.07'
timeout --kill-after=10s 60s perl <<'PERL'
use strict;
use warnings;
use App::Control;
use Digest::SHA qw(sha256_hex);
use File::Temp qw(tempdir);
print "1..2\n";
die "module version" unless $App::Control::VERSION eq '1.07';
my %hashes=(
  $INC{'App/Control.pm'}=>'424685ccfc458d9f37a620fd06ea1bcb1d77834a174ea4713f3a41ca55686184',
  '/usr/share/licenses/perl-App-Control/README'=>'5fe546aed299a46da718e0a649f2e1085170b723787514b721bf308dd83968fa',
  '/usr/share/licenses/perl-App-Control/perl538-Copying'=>'d77d235e41d54594865151f4751e835c5a82322b0e87ace266567c3391a4b912',
  '/usr/share/licenses/perl-App-Control/perl538-Artistic'=>'dd90d4f42e4dcadf5a7c09eea0189d93c7b37ae560c91f0f6d5233ed3b9292a2',
);
for my $path (sort keys %hashes) {
  open my $fh,'<',$path or die "$path: $!";
  binmode $fh; local $/;
  die "original module/notice hash $path" unless sha256_hex(<$fh>) eq $hashes{$path};
  print "# Original module/notice hash OK: $path\n";
}
print "ok 1 - installed version and original module/notice bytes\n";
my $dir=tempdir('app-control-smoke-XXXXXXXX',TMPDIR=>1,CLEANUP=>1);
my $exec="$dir/not-executed.pl";
open my $fh,'>',$exec or die "$exec: $!";
print {$fh} "#!/usr/bin/perl\nexit 0;\n" or die "write: $!";
close $fh or die "close: $!";
chmod 0755,$exec or die "chmod: $!";
my $pidfile="$dir/pids/test.pid";
my $ctl=App::Control->new(EXEC=>$exec,PIDFILE=>$pidfile,ARGS=>[]);
die "constructor" unless ref($ctl) eq 'App::Control' && -d "$dir/pids";
die "unexpected pid" if defined($ctl->pid) || $ctl->running;
die "default options" unless $ctl->{SLEEP}==1 && ref($ctl->{ARGS}) eq 'ARRAY';
die "missing-pid status" unless join('', $ctl->status) eq "$exec (no pidfile $pidfile) is not running\n";
for my $case (
  [sub {App::Control->new(PIDFILE=>$pidfile)},qr/No EXEC specified/],
  [sub {App::Control->new(EXEC=>"$dir/missing",PIDFILE=>$pidfile)},qr/doesn't exist/],
  [sub {App::Control->new(EXEC=>$exec)},qr/No PIDFILE specified/],
  [sub {App::Control->new(EXEC=>$exec,PIDFILE=>$pidfile,ARGS=>'invalid')},qr/ARGS should be an ARRAY ref/],
  [sub {$ctl->cmd('invalid')},qr/CMD should be/]
) {
  my($call,$pattern)=@$case; eval {$call->()}; die "expected constructor/argument error" unless $@ =~ $pattern;
}
open $fh,'>',$pidfile or die "pid fixture: $!";
print {$fh} "not-a-pid\n" or die "pid write: $!";
close $fh or die "pid close: $!";
eval {$ctl->pid}; die "invalid pid accepted" unless $@ =~ /looks like a funny pid/;
unlink $pidfile or die "pid unlink: $!";
print "ok 2 - private constructor/file and invalid argument behavior (no child execution)\n";
PERL
