<!-- SPDX-License-Identifier: Apache-2.0 -->
# Regexp::IPv6

Packages the authorized stable CPAN release **Regexp-IPv6 0.03** as
`perl-Regexp-IPv6` for openEuler 24.03 LTS SP3, riscv64/RVA23. The module is
pure Perl; its binary RPM is architecture-independent (`noarch`).

The exported expression follows upstream's RFC 2373 address syntax and
deliberately does **not** match the unspecified address `::`. It is not a
universal IPv6 validation API. Callers must anchor the expression when matching
an entire string; the installed smoke preserves this documented behavior.

## Source and license

- Official release: https://metacpan.org/dist/Regexp-IPv6
- Fixed source: https://cpan.metacpan.org/authors/id/S/SA/SALVA/Regexp-IPv6-0.03.tar.gz
- SHA-256: `d542d17d75ce93631de8ba2156da0e0b58a755c409cd4a0d27a3873a26712ce2`
- Discovery lineage: https://aur.archlinux.org/packages/perl-regexp-ipv6,
  version `0.03-1`, observed 2026-11-06. AUR packaging was neither copied nor
  executed; source and license evidence come from the official archive.
- `README` and `lib/Regexp/IPv6.pm` grant the same terms as Perl 5.10.0 or later:
  `GPL-1.0-or-later OR Artistic-1.0-Perl`. The README is retained as `%license`.

All seven regular members of the 3,291-byte archive were inspected, with no
links, special files or path escapes. SHA-256 matches both MetaCPAN metadata
and the publisher CHECKSUMS entry. There is no detached archive signature.
The historical CHECKSUMS index signature was verified against the official
PAUSE key at https://www.cpan.org/modules/04pause.html, primary fingerprint
`2E66557AB97C19C791AF8E20328DA867450F89EC`. GnuPG reports `VALIDSIG` together
with current `EXPKEYSIG`; this advisory index signature is not an unexpired-key
claim and does not replace mandatory pinned archive SHA-256 verification.

## Dependencies and tests

Build dependencies are `make`, `perl`, `perl-ExtUtils-MakeMaker`,
`perl-Test-Simple` (for `Test::More`) and `perl-generators`, all supplied by the
official target repository. Fresh state/repomd checks on 2026-11-06 confirmed
the official and supplemental provider indexes had not changed and contained
no matching RPM name, module provider or installed-module path.

The complete original `make test` entrypoint remains intact: 198 assertions
passed in an isolated macOS arm64 Perl 5.34.1 source-only run without runtime
skips. Upstream also contains a disabled `TODO: if (0)` maximal-match block;
it remains unchanged and is not counted as executed coverage. No downstream
test filtering, patch or added skip is used.

Real RISC-V build, original default tests, RPM installation, installed smoke
and physical RPM/SRPM acceptance remain CI gates. The host run is not target
RPM evidence. No local RPM/QEMU build was performed.
