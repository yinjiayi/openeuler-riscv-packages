<!-- SPDX-License-Identifier: Apache-2.0 -->
# gsl

This directory packages GNU GSL `2.8` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official immutable GNU release archive is independently
SHA-256 pinned and passed single-root, path, link, and special-entry safety
inspection. Committed snapshot
`discovery-20260808T165000Z-9a89920c269462cd` is the immutable source of the
manifest's `2026-08-08T16:50:00Z` lineage. It records Arch `2.8-1`, AUR
`mingw-w64-gsl` `2.8-1`, Debian `2.8+dfsg-5`, Fedora `2.8-3.fc44`, openSUSE
`2.8-5.4`, and Ubuntu `2.8+dfsg-6`. The official GNU 2.8 archive verification
is a separate hard gate, not a rewritten snapshot observation.

AUR was captured as metadata only. Its MinGW row is non-native cross-target
metadata and was excluded as a source; no PKGBUILD or distribution spec was executed. The
build retains Fedora's `riscv64` `-ffp-contract=off` setting to avoid
architecture-dependent fused-operation changes. Fedora's old patches that
relax numerical test tolerances were reviewed but deliberately not imported,
so every upstream numerical assertion and the full `make check` suite remain
unchanged. Installed smoke validates both version helpers and computes a known
special-function value through the public API.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
