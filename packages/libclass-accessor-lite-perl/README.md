<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-class-accessor-lite

This directory packages upstream `https://metacpan.org/dist/Class-Accessor-Lite` version `0.08` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

## Source and license

The fixed official CPAN archive is 30,014 bytes with SHA-256
`75b3b8ec8efe687677b63f0a10eef966e01f60735c56656ce75cbb44caba335a`,
matching the publisher's CHECKSUMS entry. The 2026-10-29 SHA-512 signed index
was verified with signing subkey `4584D789E682F9F53B392F1837D079412CC9032E`
cryptographically bound to official PAUSE primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`. This is an index signature,
not a detached signature over this archive. The source-only tool's signature
field remains advisory; its archive SHA-256 is mandatory.

Kazuho Oku's original module POD and README explicitly grant redistribution
under Perl's terms (GPL-1.0-or-later OR Artistic-1.0-Perl). README is retained
as the binary RPM's license evidence; no standalone LICENSE is invented.
The twelve bundled build-only installer files are not installed in the RPM.
Their code matches the following original, explicitly Perl-licensed releases
after ignoring only POD, generated line directives and blank lines:

- [Module-Install 1.14](https://cpan.metacpan.org/authors/id/B/BI/BINGOS/Module-Install-1.14.tar.gz), SHA-256 `3f02f0a33603aff2f5cf06d15f74d1a9be65e844ada99e1a9c2102330ffa0d49`; original README contains the copyright and permission grant.
- [Module-Install-ReadmeFromPod 0.22](https://cpan.metacpan.org/authors/id/B/BI/BINGOS/Module-Install-ReadmeFromPod-0.22.tar.gz), SHA-256 `9033c2863c2f989232279e086db2f4b3e099be8033d6b777aa1f29ed81f2deff`; original module POD contains its copyright and permission grant.

Discovery lineage is frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd`,
Ubuntu `libclass-accessor-lite-perl` 0.08-3. Current official release identity,
all open PR canonical package paths and target provider/module/manpage namespaces
were checked independently. Distribution packaging was not executed.

## Build and tests

The original Makefile.PL and default `make test` are retained without source
patches or exclusions. `-I.` makes the bundled installer import explicit on
modern Perl; `PERL_AUTOINSTALL=--skipdeps` prevents CPAN dependency installation,
not tests. Required core Perl/MakeMaker/Test::More dependencies are explicit RPM
build dependencies supplied by the target repositories. All four original test
files (26 assertions) passed on host Perl 5.34.1; that is not target-build proof.

Installed smoke covers constructor, version, read/write, read-only, write-only
and multi-value accessor behavior. No local RPM/QEMU/container build is used.
RISC-V status remains unknown until exact-head CI builds RPM/SRPM, executes the
original tests, installs the RPM and runs the committed installed smoke.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
