<!-- SPDX-License-Identifier: Apache-2.0 -->
# libarray-unique-perl

This package maps the frozen inventory's exact `libarray-unique-perl` key
to the official [Array-Unique 0.09](https://metacpan.org/dist/Array-Unique)
CPAN release. The official CPAN `CHECKSUMS` SHA-256 and an independent HTTPS
download agree on `653ce782b482800ece0bb0558e98f7a8f1986f41631261b9bb1598ab7accddf7`.
The archive has one top-level tree, only regular files and directories, and
no traversal paths. Its README and module POD grant the same GPL/Artistic
choice as Perl; there is no separate LICENSE file. CI verifies the pinned
source before building for openEuler 24.03 LTS SP3 riscv64/RVA23.

The SHA-256-verified official target Everything primary metadata contains
neither a `perl-Array-Unique` RPM nor a `perl(Array::Unique)` provider. This
target check is distinct from the frozen inventory's external Ubuntu
discovery record.

The upstream default suite has four t/ files and 184 assertions across
regular, class, unique, and false-value behavior. `%check` also runs the two
separate xt/ POD syntax and coverage suites, with target dependencies
declared so they cannot silently skip. `xt/critic.t` is an optional author
style check requiring Test::Perl::Critic, unavailable in the official target
repository; it is not claimed as passing. The upstream-provided
Module::Build route installs the library without placing development-only
`benchmark.pl` and `dev.pl` into the Perl vendor module path, unlike its
generated compatibility Makefile.PL. The installed-RPM smoke checks
uniqueness and a variant module. Local pure-Perl default tests passed;
target POD and RPM/QEMU results require exact-head CI. PR CI artifacts do
not establish public RPM repository publication.
