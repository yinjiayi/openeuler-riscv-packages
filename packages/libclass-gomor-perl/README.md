<!-- SPDX-License-Identifier: Apache-2.0 -->
# Class::Gomor 1.03

Frozen Debian `libclass-gomor-perl` 1.03-3 lineage maps to this official
stable CPAN release. The publisher's `CHECKSUMS` and the 11,710-byte
HTTPS archive agree on SHA-256
`47db3cea9ce9ffa98bf9c74557fd32cf700791ab537020c958ac30b4a9ff200b`.

The top-level `LICENSE` grants Artistic 1.0 redistribution for “This
program” and includes `LICENSE.Artistic`. Each installed PM repeats the
Artistic grant; the tests, example and build metadata have no contrary
notice or vendored code. This distribution-wide grant covers the archive.

The SHA-bound official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has
no `perl-Class-Gomor` name or `perl(Class::Gomor)` provider. It has all hard
build and runtime providers, notably `perl(Module::Build)` 0.4234,
`perl(Data::Dumper)` 2.183, `perl(Test::Pod)` 1.52,
`perl(Test::Pod::Coverage)` 1.10 and `perl(Pod::Coverage::CountParents)`.

All thirteen original test files remain unchanged. Ten functional files
exercise constructors and cloning, but several use only unconditional
`ok(1)` after printing, so their PASS is not enough to establish clone
correctness. Both POD files must run on target; the original
`t/04-test-kwalitee.t` checks distribution metadata quality only and
self-skips because target `perl(Test::Kwalitee)` is absent. The skip is
retained and disclosed, not removed or reclassified as a functional pass.

The official release's `Class::Gomor::Hash::cgFullClone` has a general Perl
assignment-precedence bug: a nested Gomor object remains aliased to its
source. A source-local patch assigns the conditional result once. This is
not a RISC-V-specific compatibility fix. The unmodified upstream Hash
case was reproduced failing by object identity; the patch was verified
locally for both Hash and Array, and the installed smoke checks accessors,
shallow clone and nested full clone identities and values for both. Target
CI must prove the physical RPM/SRPM, POD execution, and installed smoke.
No local RPM/QEMU build or publication occurred.
