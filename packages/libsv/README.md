<!-- SPDX-License-Identifier: Apache-2.0 -->
# libsv

This directory packages upstream `https://github.com/uael/sv` version `1.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed official `v1.2` commit is `3dfbda36428a7631025aaa0acef41e681824e9d1`.
The codeload archive SHA-256 is
`b5fe36e848286a543348b2a8c756f3d24bf84701729eb319cd99e4f627831e39`.
All 36 archive files were matched to Git blobs; four explicitly export-ignored
Git configuration files were fetched separately for source review, not invented
as archive members. Upstream code and test sources carry the Unlicense; the
packaged license is the original `UNLICENSE`. No upstream patch is applied.

Release version means the stable tag used for the RPM (1.2). Library version
means the original CMake `VERSION` and pkg-config version (1.0.0), and ABI version
means its `SOVERSION` (1). These upstream values are deliberately not rewritten.
CMake 3.25 or newer is required by upstream's `block()` despite its older
declared minimum. The supplier witness contains CMake 3.27.9 and ten build roots
with a conservative 122-package dependency closure; this is availability
evidence, not a successful target DNF transaction.

The original CMake default shared-library build and all seven original CTest
programs (`version`, `comp`, `match`, `range`, `semvers`, `utils`, `usage`) are
retained. Release optimization is preserved and `-UNDEBUG` keeps original test
assertions active. The same byte-verified unmodified sources run against staged
and installed libraries. Installed checks require RPM ownership/integrity and
resolve `libsv.so.1` to the RPM-owned library, without source-tree fallback.

Only repository validation and inert source verification run locally. Actual
riscv64 build, the seven default tests, staged/installed checks, RPM/SRPM
artifacts, mainline merging and public publication remain separate CI gates.
