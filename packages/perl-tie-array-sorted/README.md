<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-tie-array-sorted

This directory packages upstream `https://metacpan.org/dist/Tie-Array-Sorted` version `1.41` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Official fixed source:
`https://cpan.metacpan.org/authors/id/T/TM/TMTM/Tie-Array-Sorted-1.41.tar.gz`.
The archive SHA-256
`a99b844f68b0fa4685a445782c4891ba82c1af7dbee41ea743d4e2649f21ab7b`
matches actual bytes, MetaCPAN release metadata and TMTM's CHECKSUMS index.
The available index has a historical 2021 SHA-1 signature that verifies
mathematically to the officially published PAUSE primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`, with an expired signing subkey.
This is not a current strong signature or an archive detached signature;
`sources.yaml` records it as advisory while requiring the archive SHA-256.
The primary identity anchor is `https://www.cpan.org/modules/04pause.html`.

Discovery lineage is Debian stable (trixie) `libtie-array-sorted-perl` 1.41-5:
`https://packages.debian.org/trixie/libtie-array-sorted-perl`. External packaging
was not executed or copied. Current managed directories, all open PR
titles/files and official/supplemental target Provides/file namespaces were
checked, including the Lazy submodule and Debian/RPM naming aliases.

Although older release metadata lacks a license field, the source README and
main module explicitly grant GPL version 2 or later, copyright Simon Cozens
and Tony Bowden. This source grant establishes `GPL-2.0-or-later`; permission
is not inferred from the metadata. The README is retained as installed license
evidence. The complete GNU GPL v2 text is a separately SHA-256-pinned
Source1, copied verbatim and installed with the original notice. There is no
bundled third-party build helper. Upstream documentation
describes the component as effectively unmaintained; this recipe does not
claim renewed upstream maintenance.

All original default tests are retained. `%check` runs unmodified `make test`:
52 functionality assertions plus 2 POD and 2 POD-coverage assertions. Both
upstream-optional documentation test providers are explicitly available and
declared as BuildRequires, so neither test is intentionally skipped. The
56 assertions passed on the host with isolated official, SHA-verified pure-Perl
test-support libraries; that is not target RPM evidence. Makefile.PL does not
auto-install CPAN dependencies. The recipe requires no build-time network;
`network_during_build: false` records that requirement, not physical network
isolation by target CI.

The smoke test covers the installed version, eager/lazy numeric ordering,
duplicates and mutations. No source patch is required. Pure-Perl functionality
uses the normal QEMU-user target profile; actual RISC-V RPM build, original
tests, installation and smoke remain CI acceptance gates.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
