#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
package="${1:-perl-Test-Assertions}"
test "$package" = perl-Test-Assertions
case "$(rpm -q --qf '%{VERSION}-%{RELEASE}' "$package")" in
  1.054-1*) ;;
  *) printf 'Unexpected installed package version\n' >&2; exit 1 ;;
esac
rpm -q --provides "$package" | grep -Fx 'perl(Test::Assertions) = 1.054'
rpm -q --provides "$package" | grep -Fx 'perl(Test::Assertions::TestScript) = 1.018'
licenses="/usr/share/licenses/$package"
printf '%s  %s\n' \
  204d8eff92f95aac4df6c8122bc1505f468f3a901e5a4cc08940e0ede1938994 "$licenses/COPYING" \
  172297206f9117d3c7e6d0d151662dfc104086ef261e4558b3edd788582ab922 "$licenses/README" \
  c12dfd1946a7f39561d901e36cb4e06f55d9d2a240201675aae72ffdf40ab3bc "$licenses/Changes" \
  b0be215923c8d8545bea09d0fc529b73e2f07adeabecfed55071b2d1ca587ba2 "$licenses/Assertions.pm" \
  2d6fbe83c1af208a38e29e3b95a571b86798ca59d92088da5aa27e4d0fcab1fa "$licenses/TestScript.pm" \
  928bba10052907e4c1a91444ee1f7eecb11c2c740948d445d0b85036125f96b0 "$licenses/Manual.pod" | sha256sum --check --strict
perl <<'PERL'
use strict;
use warnings;
use Test::Assertions ();
use Test::Assertions::TestScript ();
use IO::CaptureOutput ();
use Digest::SHA qw(sha256_hex);
use File::Temp qw(tempdir);
die 'Assertions runtime version' unless $Test::Assertions::VERSION eq '1.054';
die 'TestScript runtime version' unless $Test::Assertions::TestScript::VERSION eq '1.018';
for my $module ('Test/Assertions.pm', 'Test/Assertions/TestScript.pm') {
    die "missing installed module $module" unless defined $INC{$module};
    open my $fh, '<', $INC{$module} or die "open module: $!";
    binmode $fh;
    local $/;
    my $raw = <$fh>;
    my $expected = $module eq 'Test/Assertions.pm'
      ? 'b0be215923c8d8545bea09d0fc529b73e2f07adeabecfed55071b2d1ca587ba2'
      : '2d6fbe83c1af208a38e29e3b95a571b86798ca59d92088da5aa27e4d0fcab1fa';
    die "installed raw bytes $module" unless sha256_hex($raw) eq $expected;
}
die 'deep equality' unless Test::Assertions::EQUAL({a=>[1,2]}, {a=>[1,2]});
die 'deep inequality' if Test::Assertions::EQUAL([1,2], [2,1]);
for my $case (
    [ ['1..2', 'ok 1', 'ok 2'], 1 ],
    [ ['1..2', 'ok 1', 'not ok 2'], 0 ],
    [ ['1..3', 'ok 1', 'ok 2'], 0 ]
) {
    my $result = scalar Test::Assertions::ASSESS($case->[0], 'smoke');
    my ($pass, $description) = Test::Assertions::INTERPRET($result);
    die 'ASSESS/INTERPRET semantics' unless !!$pass == !!$case->[1] && length($description);
}
my $dir = tempdir('assertions-smoke-XXXXXXXX', TMPDIR=>1, CLEANUP=>1);
die 'private fixture path must be shell-safe' unless $dir =~ m{\A/[A-Za-z0-9_./-]+\z};
my ($a, $b, $regex) = map "$dir/$_", qw(a.dat b.dat regex.dat);
die 'WRITE_FILE' unless Test::Assertions::WRITE_FILE($a, "hello\n") && Test::Assertions::WRITE_FILE($b, "hello\n");
die 'READ_FILE' unless Test::Assertions::READ_FILE($a) eq "hello\n";
die 'FILES_EQUAL positive' unless Test::Assertions::FILES_EQUAL($a, $b);
die 'EQUALS_FILE positive' unless Test::Assertions::EQUALS_FILE("hello\n", $a);
die 'regex fixture' unless Test::Assertions::WRITE_FILE($regex, 'h[ae]llo');
die 'MATCHES_FILE positive' unless Test::Assertions::MATCHES_FILE('hello', $regex);
die 'MATCHES_FILE negative' if Test::Assertions::MATCHES_FILE('prefixhello', $regex);
die 'unequal fixture' unless Test::Assertions::WRITE_FILE($b, 'different');
die 'FILES_EQUAL negative' if Test::Assertions::FILES_EQUAL($a, $b);
die 'EQUALS_FILE negative' if Test::Assertions::EQUALS_FILE('different', $a);
die 'READ_FILE missing negative' if defined Test::Assertions::READ_FILE("$dir/missing");
die 'DIED positive' unless Test::Assertions::DIED(sub { die "expected\n" });
die 'DIED negative' if Test::Assertions::DIED(sub { return 1 });
my ($good, $bad, $tapgood, $tapbad) = map "$dir/$_", qw(good.pl bad.pl tapgood.pl tapbad.pl);
die 'good compile fixture' unless Test::Assertions::WRITE_FILE($good, 'use strict; my $answer = 42;');
die 'bad compile fixture' unless Test::Assertions::WRITE_FILE($bad, 'use strict; my $broken = ;');
for my $capture (0, 1) {
    my $stderr = '';
    my ($ok, $out) = Test::Assertions::COMPILES($good, 1, $capture ? \$stderr : undef);
    die "COMPILES positive mode=$capture" unless $ok;
    die 'captured positive stderr' if $capture && $stderr !~ /syntax OK/;
    $stderr = '';
    ($ok, $out) = Test::Assertions::COMPILES($bad, 1, $capture ? \$stderr : undef);
    die "COMPILES negative mode=$capture" if $ok;
    die 'captured negative stderr' if $capture && !length($stderr);
}
die 'TAP positive fixture' unless Test::Assertions::WRITE_FILE($tapgood, 'print "1..2\nok 1\nok 2\n";');
die 'TAP negative fixture' unless Test::Assertions::WRITE_FILE($tapbad, 'print "1..2\nok 1\nnot ok 2\n";');
my ($positive) = Test::Assertions::ASSESS_FILE("$^X $tapgood", 0, 10);
my ($negative) = Test::Assertions::ASSESS_FILE("$^X $tapbad", 0, 10);
die 'ASSESS_FILE expected outcomes' unless $positive && !$negative;
print "Installed versions/module/notice bytes and deep/TAP/file/compile negative semantics OK\n";
PERL
