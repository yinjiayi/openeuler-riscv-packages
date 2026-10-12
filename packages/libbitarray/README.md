<!-- SPDX-License-Identifier: Apache-2.0 -->
# libbitarray

This directory packages BitArray 2.0 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official tag `2.0` resolves to commit
`560ed785a0687b35301a8c23b8bb9fc06b69d827`. The HTTPS archive is
SHA-256 pinned; its paths and license were reviewed. The included `LICENSE`
is CC0 1.0, consistent with the public-domain notices in the C sources.
The earlier automated discovery label `license-blocked` was not a finding
about this reviewed archive.

Upstream only ships a static library. The package also links its PIC object
into a versioned shared library, keeping the original static library for
development. The default upstream `make test` runs the bit-array,
threaded bit-lock, C example, and C++ example tests. The additional
`bitlock_try_test` binary is run explicitly. Installed smoke compiles and
runs a separate consumer against the shared library.

No external distribution recipe or AUR script is executed. CI must establish
RISC-V build, test, and install results; this README does not claim those
results in advance. Source and binaries remain under the upstream CC0 terms.
