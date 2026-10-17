#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export PATH=/usr/bin:/bin
rpm -q perl-Logfile-Rotate
rpm -q --provides perl-Logfile-Rotate | grep -F 'perl(Logfile::Rotate) = 1.05'
rpm -qf /usr/bin/gzip /usr/bin/setpriv
test -x /usr/bin/gzip
test -x /usr/bin/setpriv
printf '%s\n' \
  '9512c99bc532826dd5ff71bab274f0fa30cd0b13b1d0af6ba8c45213cbbd4a2d  /usr/share/licenses/perl-Logfile-Rotate/README' \
  '32a1fb4baa9c45524739a332de43df212283550218ebe56ec820074ce381f449  /usr/share/licenses/perl-Logfile-Rotate/Logfile-Rotate.man.html' \
  '1fdc8814234f51e186d16241b0c47e16f2013c03aae59119e1ebe5a4cc3ec36a  /usr/share/licenses/perl-Logfile-Rotate/Changes' \
  '2facb36fac40a6c53964b1459d909d72a65665b95cb3bb1e531cd1dc74af39a2  /usr/share/licenses/perl-Logfile-Rotate/perl-5.8.7-README' \
  'b7fd9b73ea99602016a326e0b62e6646060d18febdd065ceca8bb482208c3d88  /usr/share/licenses/perl-Logfile-Rotate/perl-5.8.7-Artistic' \
  '9e57f5bc2cfc54e08afc80163c29006f38d9f9c890ebd4efe3c25f0d48b65a52  /usr/share/licenses/perl-Logfile-Rotate/perl-5.8.7-Copying' | sha256sum -c -

# A fresh smoke image need not contain the build user's passwd entry.
# Numeric setpriv needs no account creation; private files are created AFTER dropping.
oe_smoke_identity=(/usr/bin/perl)
oe_expected_uid="$(id -u)"
oe_expected_gid="$(id -g)"
oe_cleared_groups=0
if [ "$(id -u)" -eq 0 ]; then
  oe_smoke_identity=(/usr/bin/setpriv --reuid=10001 --regid=10001 --clear-groups --no-new-privs /usr/bin/perl)
  oe_expected_uid=10001
  oe_expected_gid=10001
  oe_cleared_groups=1
fi
/usr/bin/timeout 120 "${oe_smoke_identity[@]}" - "$oe_expected_uid" "$oe_expected_gid" "$oe_cleared_groups" <<'PERL'
use strict;
use warnings;
use File::Temp qw(tempdir);
use Compress::Zlib qw(gzopen);
use Logfile::Rotate;
my($uid,$gid,$cleared)=@ARGV;
my @real_groups=split /\s+/, $(;
my @effective_groups=split /\s+/, $);
die "smoke must be expected ordinary UID/GID" unless $uid>0 && $gid>0 && $<==$uid && $>==$uid && $real_groups[0]==$gid && $effective_groups[0]==$gid;
die "root supplementary group" if grep {$_==0} (@real_groups,@effective_groups);
die "supplementary groups not cleared" if $cleared && (@real_groups!=1 || @effective_groups!=1);
print "Smoke identity realUID=$< effectiveUID=$> realGIDs=$( effectiveGIDs=$) cleared=$cleared\n";
die "wrong embedded module version" unless $Logfile::Rotate::VERSION eq '1.05';
umask 0077;
my $dir=tempdir('oe-logfile-rotate-XXXXXX', TMPDIR=>1, CLEANUP=>1);
die "unsafe private directory" unless -d $dir && ((stat $dir)[2]&0777)==0700 && (stat $dir)[4]==$>;
sub put { my($p,$data)=@_; open my $f,'>',$p or die $!; print {$f} $data or die $!; close $f or die $!; }
sub get { my($p)=@_; open my $f,'<',$p or die $!; local $/; my $data=<$f>; close $f or die $!; return $data; }
sub gunzip_bytes { my($p)=@_; my $z=gzopen($p,'rb') or die "gzopen $p"; my($buf,$data)=('',''); while (my $n=$z->gzread($buf)) { die "gzread" if $n<0; $data.=$buf; } $z->gzclose()==0 or die "gzclose"; return $data; }
for my $mode ('no','lib','/usr/bin/gzip') {
  my $file="$dir/".($mode eq '/usr/bin/gzip' ? 'external' : $mode).'.log';
  my($pre,$post)=(0,0);
  put($file,"first\n");
  my $log=Logfile::Rotate->new(File=>$file,Count=>2,Gzip=>$mode,Flock=>'yes',Persist=>'yes',Pre=>sub{die "pre filename" unless $_[0] eq $file; ++$pre},Post=>sub{die "post filename" unless $_[0] eq $file; ++$post});
  for my $value ("first\n","second\n","third\n") { put($file,$value); $log->rotate() or die "rotate"; my $size=-s $file; die "truncate" unless defined($size) && $size==0; }
  undef $log;
  die "callback count" unless $pre==3 && $post==3;
  my $ext=$mode eq 'no' ? '' : '.gz';
  my $latest=$mode eq 'no' ? get("$file.1$ext") : gunzip_bytes("$file.1$ext");
  my $previous=$mode eq 'no' ? get("$file.2$ext") : gunzip_bytes("$file.2$ext");
  die "rotation bytes/retention" unless $latest eq "third\n" && $previous eq "second\n" && !-e "$file.3$ext";
}
my $plain="$dir/relocate.log"; put($plain,"relocated\n");
my $rel=Logfile::Rotate->new(File=>$plain,Dir=>"$dir/old",Gzip=>'no',Flock=>'no',Persist=>'no');
$rel->rotate() or die "relocate"; undef $rel;
die "relocation bytes/mode" unless get("$dir/old/relocate.log.1") eq "relocated\n" && ((stat "$dir/old")[2]&0777)==0700;
for my $args ({}, {File=>$plain,Pre=>'invalid'}, {File=>$plain,Post=>'invalid'}, {File=>$plain,Signal=>'invalid'}, {File=>$plain,Signal=>sub{1},Post=>sub{1}}) {
  my $ok=eval { Logfile::Rotate->new(%$args); 1 }; die "invalid args accepted" if $ok || !$@;
}
my $bad=Logfile::Rotate->new(File=>$plain,Gzip=>'no',Pre=>sub{die "expected callback failure"});
my $ok=eval { $bad->rotate(); 1 }; die "callback failure swallowed" if $ok || $@!~/expected callback failure/;
undef $bad;
print "Logfile::Rotate installed private-file semantics OK (ordinary UID $>; module1.05/archive1.04)\n";
PERL
