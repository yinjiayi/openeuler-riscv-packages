<!-- SPDX-License-Identifier: Apache-2.0 -->
# libhash-asobject-perl

The frozen inventory's `libhash-asobject-perl` key (Ubuntu and Debian source
0.13-4) maps to official stable [Hash-AsObject 0.13](https://metacpan.org/dist/Hash-AsObject).
The official HTTPS archive SHA-256 is
`36dafa4bc61207ad2959bc736c747f0b4ff595c5b5b65cb26d917b15732dcb8d`,
identical to publisher `CHECKSUMS`. All archive entries are regular files or
directories under one root, with no links or traversal paths. The bundled
README and module grant Perl terms; Makefile.PL and META.yml agree. The
frozen distribution record did not resolve the license, so the spec uses
these independently checked upstream declarations.

The official openEuler 24.03 LTS SP3 `riscv64`/RVA23 `everything` primary
metadata SHA-256 is
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
It contains neither `perl-Hash-AsObject` nor `perl(Hash::AsObject)`, and
includes all declared build/test dependencies, including POD coverage.
This is a snapshot collision check, not a future guarantee.

`%check` retains all ten default upstream test files. They passed with 98
assertions on local Perl 5.34.1 after temporarily installing four
SHA-verified official CPAN test-only dependency archives to exercise the
otherwise optional POD-coverage test. The target SP3 repository already
provides those dependencies. The installed-RPM smoke checks the module
provider and accessor/mutator API. Exact-head target CI must still establish
the SP3 RVA23 RPM build, complete suite and installed smoke; no local
RPM/QEMU result is claimed.
