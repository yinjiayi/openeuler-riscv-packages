<!-- SPDX-License-Identifier: Apache-2.0 -->
# FTXUI

This directory packages the stable FTXUI 7.0.3 release for openEuler 24.03
LTS SP3 on `riscv64`/RVA23. The official GitHub tag archive is pinned by
SHA-256 in `sources.yaml`. Its only link is `bazel/test/.bazelrc`, whose
relative target remains inside the archive root.

FTXUI requires static libraries when compiling its registered unit tests
because those tests access internal symbols hidden by the shared-library
build. The SPEC therefore uses two independent CMake build trees: a shared
install tree that produces the RPM payload, and a static test tree that is
never installed. The test tree builds and runs every test registered by
upstream CTest. It also compiles upstream's benchmark target using the exact
Google Benchmark 1.8.2 revision named by FTXUI, pinned as a test-only Source1;
no performance claim is made and no source is downloaded during the build.

The installed smoke test checks the three runtime libraries, public headers,
pkg-config and CMake metadata, then compiles and runs a small C++17 consumer
that renders an FTXUI DOM document.

External source licenses remain those of FTXUI and its test dependency. The
repository license covers only this packaging metadata and smoke-test code.
