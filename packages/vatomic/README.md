<!-- SPDX-License-Identifier: Apache-2.0 -->
# vatomic

This directory packages upstream `https://github.com/open-s4c/vatomic` version `2.4.1` release `7` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The build uses the upstream `VATOMIC_TESTS` option and includes the C++ compiler required by the C++11 test programs. Developer-time template regeneration is disabled during RPM construction, so the package installs the generated headers already present in the SHA-256-verified release archive while retaining the upstream C, C++, and RISC-V-aware test suite. Release `3` explicitly configures CMake in the build directory consumed by the openEuler RPM macros. Release `4` requires the fixed target repository's `libatomic` runtime because upstream links its RISC-V 8-bit and 16-bit atomic tests with `-latomic`. Release `5` preserves the complete upstream test suite while making its `std::atomic` mirror comparisons valid under `_GLIBCXX_ASSERTIONS`: store operations map `consume`, `acquire`, and `acq_rel` to `relaxed`, and load operations map `release` and `acq_rel` to `relaxed`, for both mirror and subject. No upstream feature or test is removed.

Release `6` removes an excess context line from the first patch hunk so strict GNU patch 2.8 applies the unchanged test fix.

Release `7` extends the same test-only correction to compare-exchange: a `release` success uses a `relaxed` failure order, an `acq_rel` success uses an `acquire` failure order, and every other failure order remains unchanged. Success orders are unchanged, both the `std::atomic` mirror and vatomic subject receive the same mapping, and all 240 upstream tests remain enabled.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
