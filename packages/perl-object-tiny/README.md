<!-- SPDX-License-Identifier: Apache-2.0 -->
# Object::Tiny 1.09

This directory packages upstream `https://metacpan.org/dist/Object-Tiny` version `1.09` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Source and license

The fixed official author archive is
`https://cpan.metacpan.org/authors/id/E/ET/ETHER/Object-Tiny-1.09.tar.gz`.
Its 28,377 bytes have SHA-256
`7819ccdd18ee18b0e5ce660c084e4e04be3f2f34341302925581d21b53cac6bd`,
matching the verified publisher CHECKSUMS plaintext. The index's SHA-512
signature verifies through signing subkey
`4584D789E682F9F53B392F1837D079412CC9032E` to official PAUSE primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`. This is a signed index, not a
detached archive signature. CI requires the pinned archive SHA-256 and records
the index as advisory; the independent operator signature check is separate.

The original LICENSE, README and module POD explicitly grant Adam Kennedy's
code under Perl's GPL-1.0-or-later OR Artistic-1.0-Perl terms. The package has
no bundled third-party implementation. The original LICENSE is installed.

Frozen discovery `discovery-20260808T165000Z-9a89920c269462cd` retains Debian
`libobject-tiny-perl` 1.09-1 and Fedora `perl-Object-Tiny` 1.09-22.fc44 lineage.
No distribution recipe was executed. Current managed packages, complete open
PR aliases/titles/paths and target provider/file namespaces were checked for
collisions before acquisition and again before submission.

## Recipe and tests

This is a pure-Perl noarch module. The recipe uses the release's generated
Makefile.PL; Dist::Zilla is only an upstream authoring dependency, not a build
dependency of the shipped release. Target packages supply all default test
requirements and CPAN::Meta for the original prerequisite diagnostics.

`%check` retains the complete upstream `make test`: four files and 28 assertions.
The original `xt/` author/release tests and example benchmark are not part of
that default target; no default test is removed or disabled. All 28 assertions
passed on host Perl, which is not target RPM build or installation evidence.
The installed smoke checks the version, constructor, read-only accessors and
rejection of an invalid accessor name. No source patch is required.

Exact-head CI must still establish the target build, original tests and
installed smoke; physical RPM/SRPM acceptance remains a separate merge gate.
