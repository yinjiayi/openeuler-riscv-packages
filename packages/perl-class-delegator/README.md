<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-class-delegator

This directory packages upstream `https://metacpan.org/dist/Class-Delegator` version `0.09` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Source, license and naming

The fixed official CPAN archive `Class-Delegator-0.09.tar.gz` has SHA-256
`6dfd85cc78e844f14b20602233501cdd052f4d794b733db0d6bc0ae434b671ed`.
Its README and module POD explicitly grant David Wheeler's 2005-2008 work
under the same terms as Perl; original notices are retained. The original
CHECKSUMS index signature validates against the official PAUSE primary anchor
`2E66557AB97C19C791AF8E20328DA867450F89EC`, and its entry matches the archive's
hash and size. That is an index signature, not a detached archive signature.
The source SHA-256 is mandatory under the policy in sources.yaml.

The discovery catalog records Debian stable `libclass-delegator-perl` 0.09-6.
Complete normalized open-PR title/current-and-previous-file inventories,
managed IDs and official/supplemental RPM names, provides and payload paths
were checked, including the alternative `libclass-delegator-perl` spelling.
Distribution lineage is not target build evidence.

## Generated template notice

The original Makefile.PL identifies Module::Build::Compat 0.2808_01. Its complete
bytes were matched to the exact official release's passthrough template in
`lib/Module/Build/Compat.pm`, substituting an empty subclass-loader and the class
name `Module::Build`. The auxiliary archive SHA-256 is
`e3253fcb86c56344b5b6547502f9fda6072d9c63efc33b0915eb9b48717984d2`.
That template's original Ken Williams 2001-2006 attribution and same-Perl grant
are retained in GENERATED-NOTICE by a notice-only patch. No copyright exemption
for generated output is assumed. No unrelated generator source is added to the
SRPM. The original ten source files, including Makefile.PL and every original
test, remain byte-identical. Both README and GENERATED-NOTICE ship as license
documents; the patch and unchanged archive also remain in the SRPM.

## Build and validation

The recipe invokes the original Build.PL and Build directly with the supplied
Module::Build dependency, not the generated Makefile.PL's optional CPAN-install
fallback. Target providers include Module::Build 0.42.34, Test::More 1.302198,
Test::Harness 3.48, Test::Pod 1.52 and Test::Pod::Coverage 1.10. The original
`Build test` target and all three test files are kept unchanged. Host execution
passes 100 assertions (99 functional plus POD) with the original POD-coverage
test's dependency-based skip because that optional module is absent locally;
the target BuildRequires explicitly supplies it. No skip is added by this recipe.

GNU patch with zero fuzz verifies the notice-only addition. The installed
smoke exercises renamed, scalar and list-context multiple delegation. Local
host/source-only checks do not establish target RPM build/install success;
exact-head RISC-V CI and physical artifacts are still required. The manifest
disallows build-time downloads and the direct Build.PL recipe does not fetch
dependencies; no physical network-isolation claim is made.
