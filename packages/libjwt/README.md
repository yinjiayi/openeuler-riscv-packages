<!-- SPDX-License-Identifier: Apache-2.0 -->
# libjwt

This directory packages upstream `https://github.com/benmcollins/libjwt`
version `3.6.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks AUR
(`3.2.3-2`), Fedora 44 (`1.12.1-21.fc44`), openSUSE Tumbleweed
(`1.18.3-2.3`), Debian stable (`1.17.2-1`), and Ubuntu Resolute GA
(`1.17.2-1build1`). The same snapshot was queried for Arch stable metadata
and contained no `libjwt` component; that negative result is recorded rather
than inventing a lineage row. No distribution recipe or AUR content was read
or executed.

The target provides OpenSSL 3.0.12, which satisfies libjwt's supported
OpenSSL 3.0 floor. Its GnuTLS 3.8.2 is below upstream's 3.8.8 floor, and the
experimental ML-DSA feature needs OpenSSL 3.5 or GnuTLS 3.8.10, so this package
selects the supported OpenSSL backend and leaves experimental ML-DSA disabled.
The complete resulting upstream gate is 40 registered CTest tests, including
the Bats CLI integration suite; all run without network access. Capability-
guarded ML-DSA cases remain upstream-declared skips on this dependency set,
not downstream test exclusions.

The source is the publisher's immutable release asset and its SHA-256 matches
the digest published by GitHub. No distribution source or mirror was
substituted.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
