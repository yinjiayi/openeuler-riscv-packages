#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
package="${1:-perl-Class-Accessor-Chained}"
test "$package" = perl-Class-Accessor-Chained
case "$(rpm -q --qf '%{VERSION}-%{RELEASE}' "$package")" in
  0.01-1*) ;;
  *) printf 'Unexpected installed package version\n' >&2; exit 1 ;;
esac
rpm -q --provides "$package" | grep -Fx 'perl(Class::Accessor::Chained) = 0.01'
rpm -q --provides "$package" | grep -Fx 'perl(Class::Accessor::Chained::Fast)'
licenses="/usr/share/licenses/$package"
printf '%s  %s\n' \
  4a59a6aa1729128b88991baae3e95a5c1af8489ae3ba6cfcfad3d7d3fb7a3088 "$licenses/README" \
  b9ca5c561b52d5d3bf2e7ee8c5711a297a9272d69bdeccc61b66bc3c09d7190b "$licenses/Changes" \
  ac1e9255db7e9d243891f310259dbbfaeffa2140b2f97fe2a05a0aba419c3c24 "$licenses/Chained.pm" \
  003b6ef3689e6fc5c53200a0f82d536d5d306d08e121928f6b58c8809a46944b "$licenses/Fast.pm" \
  2facb36fac40a6c53964b1459d909d72a65665b95cb3bb1e531cd1dc74af39a2 "$licenses/perl-5.8.7-README" \
  b7fd9b73ea99602016a326e0b62e6646060d18febdd065ceca8bb482208c3d88 "$licenses/perl-5.8.7-Artistic" \
  9e57f5bc2cfc54e08afc80163c29006f38d9f9c890ebd4efe3c25f0d48b65a52 "$licenses/perl-5.8.7-Copying" | sha256sum --check --strict
perl <<'PERL'
use strict;
use warnings;
use Class::Accessor::Chained;
use Class::Accessor::Chained::Fast;
use Scalar::Util qw(refaddr);
die "main module version" unless $Class::Accessor::Chained::VERSION eq '0.01';
die "invented Fast module version" if defined $Class::Accessor::Chained::Fast::VERSION;
for my $module ('Class/Accessor/Chained.pm', 'Class/Accessor/Chained/Fast.pm') {
    die "missing installed module $module" unless defined $INC{$module};
    open my $fh, '<', $INC{$module} or die "open installed module: $!";
    binmode $fh;
    local $/;
    my $bytes = <$fh>;
    require Digest::SHA;
    my $expected = $module eq 'Class/Accessor/Chained.pm'
      ? 'ac1e9255db7e9d243891f310259dbbfaeffa2140b2f97fe2a05a0aba419c3c24'
      : '003b6ef3689e6fc5c53200a0f82d536d5d306d08e121928f6b58c8809a46944b';
    die "installed module bytes $module" unless Digest::SHA::sha256_hex($bytes) eq $expected;
}
{
    package ChainedSmoke;
    use base 'Class::Accessor::Chained';
    __PACKAGE__->mk_accessors(qw(rw other));
    __PACKAGE__->mk_wo_accessors('wo');
    __PACKAGE__->mk_ro_accessors('ro');
}
{
    package ChainedFastSmoke;
    use base 'Class::Accessor::Chained::Fast';
    __PACKAGE__->mk_accessors(qw(rw other));
    __PACKAGE__->mk_wo_accessors('wo');
    __PACKAGE__->mk_ro_accessors('ro');
}
sub must_fail {
    my ($label, $call) = @_;
    my $ok = eval { $call->(); 1 };
    my $error = $@;
    die "$label did not fail" if $ok || !length($error);
}
for my $class ('ChainedSmoke', 'ChainedFastSmoke') {
    my $object = $class->new({ro => 'original'});
    die "$class constructor" unless ref($object) eq $class;
    my $result = $object->rw(11)->other(22)->wo(33);
    die "$class chain identity" unless refaddr($result) == refaddr($object);
    die "$class read/write values" unless $object->rw == 11 && $object->other == 22 && $object->{wo} == 33;
    die "$class multi-value rw identity" unless refaddr($object->rw('a', 'b')) == refaddr($object);
    my $values = $object->rw;
    die "$class multi-value rw values" unless ref($values) eq 'ARRAY' && @$values == 2 && $values->[0] eq 'a' && $values->[1] eq 'b';
    die "$class multi-value wo identity" unless refaddr($object->wo('c', 'd')) == refaddr($object);
    my $writes = $object->{wo};
    die "$class multi-value wo values" unless ref($writes) eq 'ARRAY' && @$writes == 2 && $writes->[0] eq 'c' && $writes->[1] eq 'd';
    die "$class read-only value" unless $object->ro eq 'original';
    must_fail("$class write-only read", sub { $object->wo });
    must_fail("$class read-only write", sub { $object->ro('changed') });
    die "$class failed read-only write changed value" unless $object->ro eq 'original';
    print "$class rw/wo/ro/multivalue/chaining/negative semantics OK\n";
}
PERL
