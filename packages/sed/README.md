<!-- SPDX-License-Identifier: Apache-2.0 -->
# sed

This directory packages GNU sed `4.10` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. It is the official current stable release and is newer than
the Fedora 44, Debian stable, and Ubuntu 26.04 LTS GA snapshots. Arch stable
and openSUSE Tumbleweed had already moved to 4.10 when the lineage snapshot
was frozen.

The official GNU archive is pinned by SHA-256 and passed an archive inspection
for a single expected root, safe paths and links, and no special entries. The
AUR lookup was RPC metadata only; its VCS entry was more than 24 months old
and was excluded. No AUR recipe was read or executed; distribution specs were
reviewed only as untrusted, read-only lineage evidence and were never
executed. The build deliberately uses sed's shipped GNU regex implementation so the
complete upstream tests exercise deterministic package code instead of
requiring downstream suppression of a known system-regex back-reference test.
ACL and SELinux support remain enabled, and the installed smoke test verifies
extended-regex, capture, and in-place editing behavior.

The build exports gnulib's `gl_cv_func_localeconv_works=no` configure cache
result so `configure` selects the bundled `localeconv` replacement. That
replacement normalizes openEuler RISC-V's unsigned-`char` unavailable-field
representation to the standard `CHAR_MAX` sentinel. This keeps the complete
upstream test suite enabled and preserves the interface expected by sed and
other gnulib code.

External source licenses remain those of the upstream project. The repository
license covers only original packaging metadata, scripts, and documentation.
