<!-- SPDX-License-Identifier: Apache-2.0 -->
# libhash-multivalue-perl

The frozen inventory's `libhash-multivalue-perl` key (Ubuntu source 0.16-3)
maps to official stable [Hash-MultiValue 0.16](https://metacpan.org/dist/Hash-MultiValue).
The official HTTPS archive SHA-256 is
`66181df7aa68e2786faf6895c88b18b95c800a8e4e6fb4c07fd176410a3c73f4`,
identical to publisher `CHECKSUMS`. All archive entries are regular files or
directories under one root, with no links or traversal paths. The bundled
LICENSE contains the Perl GPL-1-or-later / Artistic terms; README, module,
Makefile.PL and META.json agree.

The official openEuler 24.03 LTS SP3 `riscv64`/RVA23 `everything` primary
metadata SHA-256 is
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
It contains neither `perl-Hash-MultiValue` nor `perl(Hash::MultiValue)`, and
includes all declared build/test dependencies, including Storable and Perl
threads. This is a snapshot collision check, not a future guarantee.

`%check` retains all ten default upstream test files. They passed with 57
assertions on local Perl 5.34.1; `t/ref.t` and `t/release-pod-syntax.t` made
their own upstream-defined skips for an optional module and release-only
testing. The installed-RPM smoke checks its provider and multi-value API.
Exact-head target CI must still establish the SP3 RVA23 RPM build, complete
suite and installed smoke; no local RPM/QEMU result is claimed.
