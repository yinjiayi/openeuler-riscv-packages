<!-- SPDX-License-Identifier: Apache-2.0 -->
# dashpay-bls-signatures

This directory packages upstream `https://github.com/dashpay/bls-signatures` version `1.3.5` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The pinned tag archive expands beneath `bls-signatures-1.3.5`. This package builds the GMP-accelerated C++ library and its bundled C++ test program in one explicit out-of-source CMake directory. Optional Python bindings and benchmarks are disabled; this avoids fetching an additional unverified source during CMake configuration and keeps the RPM scoped to the Dashcore library. Packaging release 4 also disables only the empty automatic debuginfo subpackage observed after the main library and all bundled tests completed successfully; the main RPM build and test entry point remain unchanged.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
