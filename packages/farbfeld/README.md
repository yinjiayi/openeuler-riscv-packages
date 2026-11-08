<!-- SPDX-License-Identifier: Apache-2.0 -->
# farbfeld

This directory packages upstream `https://tools.suckless.org/farbfeld/` version `4` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Official fixed archive: https://dl.suckless.org/farbfeld/farbfeld-4.tar.gz,
SHA-256 `c7df5921edd121ca5d5b1cf6fb01e430aff9b31242262e4f690d3af72ccbe72a`.
All 23 upstream files were reviewed without execution. ISC covers the tools;
the bundled farbfeld.5 example carries 0BSD. Both notices remain unchanged.
No source patches or external packaging were borrowed.

The original default `all` builds all six converters, and install includes
the original `2ff` script and all eight manuals. The complete ImageMagick
fallback stays enabled with an explicit runtime dependency. Distribution
compiler/link flags retain default features and CPPFLAGS while allowing RPM
debug information. Build/check are offline and unprivileged.

Upstream 4 has no check/test target. Five added downstream functional groups
check exact PAM/PPM and alpha blending, exact PNG roundtrip plus independently
generated 8-bit PNG, bounded lossy white JPEG conversion, `2ff` including the
ImageMagick fallback, and malformed/truncated image/argument rejection.
They execute against the build, staged and normal installed binaries with
enabled Python assertions and finite child timeouts. These are not a complete
fuzz/security audit, performance measurement or native-RISC-V validation.
Local work validates metadata and checker syntax only; real target evidence
must come from the immutable openEuler 24.03 LTS SP3 RVA23 CI image.
