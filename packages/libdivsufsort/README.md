<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdivsufsort

This directory packages upstream libdivsufsort 2.0.1 for openEuler 24.03 LTS
SP3 on `riscv64`/RVA23. CI downloads the official tag archive over HTTPS and
verifies its pinned SHA-256 before the network-enabled target build.

The downstream CMake patch corrects the release version embedded in the
official tag and routes libraries and pkg-config metadata through
GNUInstallDirs. Both the 32-bit and 64-bit index APIs are packaged. `%check`
runs upstream's suffix-array verifier, while the installed-RPM smoke test
compiles and validates the canonical suffix array for `banana` through both
public APIs.

External source and patch licenses remain MIT. The repository license only
covers original packaging metadata, scripts, and documentation.
