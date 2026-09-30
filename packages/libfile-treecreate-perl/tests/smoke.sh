#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-TreeCreate
rpm -q --whatprovides 'perl(File::TreeCreate)'
test_dir="$(mktemp -d)"
trap 'rm -f -- "$test_dir/nested/message.txt"; rmdir -- "$test_dir/nested" "$test_dir"' EXIT
perl -MFile::TreeCreate -e '
  die "unexpected File::TreeCreate version\n"
    unless $File::TreeCreate::VERSION eq "0.0.1";
  File::TreeCreate->new->create_tree($ARGV[0] . "/", {
    name => "nested/", subs => [{name => "message.txt", contents => "hello\n"}]
  });
' "$test_dir"
printf 'hello\n' | cmp -s - "$test_dir/nested/message.txt"
