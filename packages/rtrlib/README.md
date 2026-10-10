<!-- SPDX-License-Identifier: Apache-2.0 -->
# rtrlib

This directory packages upstream `https://github.com/rtrlib/rtrlib` version `0.8.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The RPM build uses the openEuler out-of-source CMake macros, retains libssh transport, enables the CMocka tests, and runs all eight deterministic registered tests. The two live-service tests (`test_live_validation` and `test_dynamic_groups`) are enumerated but excluded because they require `rpki-validator.realmv6.org:8283`; the CI attempt received connection refusals from that external service. The installed smoke check covers both command-line tools, the public API, shared library, and pkg-config metadata.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
