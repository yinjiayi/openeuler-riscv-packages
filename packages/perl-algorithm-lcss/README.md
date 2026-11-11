<!-- SPDX-License-Identifier: Apache-2.0 -->
# Algorithm::LCSS

Packages the authorized stable CPAN release **Algorithm-LCSS 0.01** as
`perl-Algorithm-LCSS` for openEuler 24.03 LTS SP3, riscv64/RVA23. The module is
pure Perl and finds common contiguous subsequences in strings and arrays using
`Algorithm::Diff`; the binary RPM is architecture-independent (`noarch`).

## Source and license

- Official release: https://metacpan.org/dist/Algorithm-LCSS
- Fixed archive: https://cpan.metacpan.org/authors/id/J/JF/JFREEMAN/Algorithm-LCSS-0.01.tar.gz
- SHA-256: `717cefcc7842a171ab5576f22eb72e566edf061ceaf87dccbe7f2081f5601f78`
- Discovery lineage: https://aur.archlinux.org/packages/perl-algorithm-lcss,
  version `0.01-1`, observed 2026-11-06. AUR packaging was neither executed nor
  copied; source and permission findings come from the official CPAN archive.
- Upstream `README` grants redistribution and modification under the same terms
  as Perl itself: `GPL-1.0-or-later OR Artistic-1.0-Perl`. The grant is retained
  in the RPM as a license file.

The 4,922-byte archive SHA-256 matches both MetaCPAN release metadata and the
publisher's `CHECKSUMS` entry, including its `J/JF/JFREEMAN` path. All nine
regular archive members were inspected; no links, special files or path escapes
were present. There is no archive-level detached signature. The advisory
historical CHECKSUMS signature was cryptographically verified against the PAUSE
key published at https://www.cpan.org/modules/04pause.html, primary fingerprint
`2E66557AB97C19C791AF8E20328DA867450F89EC`. It uses SHA-1 and predates key expiry;
GnuPG now reports `VALIDSIG` together with `EXPKEYSIG`. This is not a current
unexpired-key claim and never replaces the mandatory pinned archive SHA-256.

## Dependencies and checks

Build dependencies are `make`, `perl`, `perl-ExtUtils-MakeMaker`,
`perl-Algorithm-Diff >= 1.1` and `perl-generators`. Upstream's original `Test`
module is provided by the target `perl` package. Runtime requires
`perl(Algorithm::Diff) >= 1.1`; the official target repository provides 1.201.
Fresh official and supplemental primary/filelists metadata on 2026-11-06 found
no existing RPM name, `perl(Algorithm::LCSS)` provider or module-path collision.

The SPEC retains the complete upstream `make test` entrypoint (`test.pl`, eight
assertions, no skip/exclusion directives). An isolated macOS arm64 source-only
run passed all eight assertions using Perl 5.34.1 and Algorithm::Diff 1.1903.
That host result is not target RPM evidence. Installed smoke checks the RPM and
module version plus string, array and sorted-result behavior.

No RISC-V patch or native-only validation requirement was identified from this
pure-Perl code. Real RISC-V build, default tests, installed smoke and physical
RPM/SRPM acceptance remain pending CI; no local RPM or QEMU build was run.
