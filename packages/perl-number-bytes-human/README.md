<!-- SPDX-License-Identifier: Apache-2.0 -->
# Number::Bytes::Human

Packages CPAN **Number-Bytes-Human 0.11** as `perl-Number-Bytes-Human` for
openEuler 24.03 LTS SP3, riscv64/RVA23. The module formats and parses byte
quantities in binary or decimal units. Its implementation is pure Perl and the
binary RPM is architecture-independent (`noarch`).

## Source and license

- Official release: https://metacpan.org/dist/Number-Bytes-Human
- Fixed archive: https://cpan.metacpan.org/authors/id/F/FE/FERREIRA/Number-Bytes-Human-0.11.tar.gz
- SHA-256: `5fc79c49b0b40df780479c43696381343e2b6ad1fe52859f60bc65b66ebe6f2c`
- Distribution lineage: https://packages.debian.org/trixie/libnumber-bytes-human-perl,
  version `0.11-4`, observed 2026-11-07. Debian packaging was not executed.

The actual 11,571-byte archive matches both the MetaCPAN release record and the
publisher's `CHECKSUMS` entry. All 21 archive entries were inspected; no links,
special files or path escapes were present. No bundled or detached archive
signature was identified; the pinned SHA-256 remains mandatory.

The publisher's historical CHECKSUMS index signature was verified against the
key freshly obtained from https://www.cpan.org/modules/04pause.html: primary
fingerprint `2E66557AB97C19C791AF8E20328DA867450F89EC`, signing fingerprint
`33EAEF6DBA3865943BEE9D5BB6A1739063760CCA`. GnuPG returned `VALIDSIG` and
`EXPKEYSIG` for the 2021-11-22 SHA-1 signature. This is evidence of a historical
index signature, not a current unexpired-key or detached archive-signature
claim, and never replaces the pinned archive SHA-256 check.

The copyright and license section of `Human.pm` grants redistribution and
modification under the same terms as Perl itself; `META.json` also declares
`perl_5`. The package declares `GPL-1.0-or-later OR Artistic-1.0-Perl` and retains
the original license-bearing module as a license file.

## Dependencies and validation

The build uses `make`, `perl`, `perl-ExtUtils-MakeMaker`, `perl-Carp`,
`perl-Exporter`, `perl-generators`,
`perl-Test-Simple`, `perl-Test-Pod` and `perl-Test-Pod-Coverage`. POSIX and Carp
are supplied by the target Perl packages. Upstream's declared `Test::More`
runtime prerequisite is retained. Fresh official and supplemental repository
primary/filelists metadata on 2026-11-07 found no existing RPM name,
`perl(Number::Bytes::Human)` provider or `Number/Bytes/Human.pm` path collision.

The SPEC runs the original `Makefile.PL`, build and complete `make test`
entrypoint without changing or excluding any of the twelve upstream test
files. Both optional POD-check dependencies are included in BuildRequires.
An isolated macOS arm64 run with Perl 5.34.1 passed 222 assertions across the
default test invocation; upstream's optional `t/98pod-coverage.t` skipped
because that host lacks Test::Pod::Coverage. This is a host preflight result,
not a successful target RPM build or a claim that the skipped POD check ran.

Installed smoke checks the RPM and module versions, binary formatting and
parsing, decimal SI units, and object configuration for custom zero values.
No architecture-specific code or native-only validation need was identified.
Target build, original tests, installed smoke and physical RPM/SRPM acceptance
remain pending CI. No local RPM or QEMU build was run.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
