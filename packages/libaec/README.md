<!-- SPDX-License-Identifier: Apache-2.0 -->
# libaec

This directory packages libaec `1.1.7` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official immutable release asset is independently
SHA-256 pinned, agrees with its publisher attestation, and passed single-root,
path, link, and special-entry safety inspection. Committed snapshot
`discovery-20260808T165000Z-9a89920c269462cd` is the immutable source of the
manifest's raw versions and `2026-08-08T16:50:00Z` observation time. It
records Arch `1.1.7-1`, AUR `android-riscv64-libaec` `1.1.5-1`, Debian
`1.1.3-1`, Fedora `1.1.5-1.fc44`, openSUSE `1.1.7-1.3`, and Ubuntu `1.1.5-1`.
The current official 1.1.7 verification is a separate hard gate and includes
upstream's decoder security fixes.

AUR was captured through metadata only. Its Android RISC-V row is non-native
cross-target metadata and was excluded as a source; no PKGBUILD or
distribution spec was executed.
The CMake build disables static libraries but keeps every upstream CTest case,
including code-option, buffer-size, seeking, long-fundamental-sequence, SZIP,
RSI block-access, and bundled CCSDS sample-data tests. The separate
`update-sampledata` maintenance target is not part of CTest and is never run,
so the build remains offline. Installed smoke performs a public-API encode and
decode round trip.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
