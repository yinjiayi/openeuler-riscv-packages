<!-- SPDX-License-Identifier: Apache-2.0 -->
# dashpay-bls-signatures

This directory packages upstream `https://github.com/dashpay/bls-signatures` version `1.3.5` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The pinned tag archive expands beneath `bls-signatures-1.3.5`. This package builds the GMP-accelerated C++ library and its bundled C++ test program. Optional Python bindings and benchmarks are disabled; this avoids fetching an additional unverified source during CMake configuration and keeps the RPM scoped to the Dashcore library.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
