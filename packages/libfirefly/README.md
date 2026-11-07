<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfirefly

This directory packages upstream `https://github.com/tbhaxor/firefly` version `3.1.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The canonical component is `github.com-tbhaxor-firefly`, not the older
`libfirefly2` discovery entry or an unrelated Firefly program. The frozen AUR
lineage is `libfirefly` 3.1.0-2 in discovery-20260808T165000Z-9a89920c269462cd;
no distribution recipe is executed. Official tag `v3.1.0` resolves to
`208ef838b3f9290d3d6272b476e0a15f7a6b17fb`. All 27 regular archive files
were matched to that Git tree. Archive SHA-256:
`b2c643ffb3278c958e800cacd9b4a4b6070c873e7df6b8c3eff5c195a079a1cb`.
Upstream's CMake `PROJECT_VERSION` still says 3.0.0; RPM uses the official
3.1.0 tag and does not silently edit that source value.

This header library retains C++23, both original headers, and original CMake.
The declared CMake 3.10 minimum does not cover CMP0135, so packaging requires
CMake >= 3.24 (official target provider 3.27.9), plus GCC >= 14 (14.3.1).
The fresh official 18,503 and supplemental 1,240 primary/filelists joins found
no canonical package or installed-header/private executable collision and no
missing dependency capability. These are provider checks, not a DNF/build pass.

Original tests are off by default, but upstream CI enables tests and examples;
this recipe does the same. A **complete original suite** means the unchanged
six C++ test sources with all 96 `TEST` declarations and original assertions,
executed by CTest in `%check` and again from the installed original test binary.
No exclusions, disabled cases, ignored failures or lowered language standard
are introduced. The original example is also built and executed. A **downstream
installed-header check** is the separate 10-case C++ consumer, not 10 additional
upstream tests; it compiles against staged and RPM-installed headers.

The original FetchContent declaration pins GoogleTest
`03597a01ee50ed33e9dfd640b249b4be3799d395`. Source1 is its official fixed
archive, SHA-256 `3dd5da4302b4069f90b2d58f48e6f3bc4c9938e024e7599241cafaebda476013`;
all 243 regular files were Git-blob matched. An exact
`FETCHCONTENT_SOURCE_DIR_GOOGLETEST` override and full disconnection supply
those bytes without build-time download. `INSTALL_GTEST=OFF` only prevents
this private test dependency from overwriting the system GoogleTest package;
it does not disable the Firefly tests. Source archives, licenses and complete
corresponding build inputs remain in the SRPM.

The project supplies GPLv3 text without an additional permission notice, so it
is conservatively recorded as GPL-3.0-only. GoogleTest is BSD-3-Clause; its
license accompanies the privately linked original test binary. Both original
licenses, README, headers and checksum-bound original test/example sources are
installed. This is an architecture-specific RPM because it carries original
riscv64 test/example executables, despite the library being header-only. The
documentation-only `externals/doxygen-awesome-css` gitlink is not used by the
default CMake build and is not fetched. No patch or upstream write is needed.

Local acceptance is limited to repository validation and inert source/recipe
inspection. Actual locked openEuler 24.03 LTS SP3 riscv64/RVA23 build, all
original tests, installed smoke, and physical RPM/SRPM evidence must come from
fresh CI before merge. There is no local RPM/QEMU build or native-hardware claim.
