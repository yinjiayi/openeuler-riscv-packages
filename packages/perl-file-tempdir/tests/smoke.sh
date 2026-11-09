#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
tmp=$(mktemp -d)
trap 'rm -r "$tmp"' EXIT HUP INT TERM
mkdir "$tmp/caller-owned"
TMPDIR="$tmp" perl -MFile::Tempdir -e '
  my $root = shift;
  my $path;
  {
    my $managed = File::Tempdir->new("managed-XXXXXXXX", DIR => $root);
    $path = $managed->name;
    die "managed directory not created" unless -d $path && index($path, "$root/") == 0;
    print "ok - creates managed directory\n";
  }
  die "managed directory retained" if -e $path;
  print "ok - destroys managed directory\n";
  my $caller = "$root/caller-owned";
  {
    my $wrapped = File::Tempdir->new($caller);
    die "caller directory changed" unless $wrapped->name eq $caller;
  }
  die "caller directory removed" unless -d $caller;
  print "ok - preserves caller-owned directory\n";
' "$tmp"
