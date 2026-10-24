<!-- SPDX-License-Identifier: Apache-2.0 -->
# libspatialindex

This directory packages upstream `https://libspatialindex.github.io` version `2.1.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The stable official tag `2.1.0` resolves to commit
`175b56a9541e76982d13dbbf0c9b8f0b8d752619`. Its fixed codeload archive
has SHA-256 `35756700f88fa12368b38ed2580acf24ad6fe95111744ac7f21c83f6955cb6ee`;
all 325 regular archive members match the corresponding Git blobs. No detached
signature is claimed. Discovery retains the frozen Arch extra `2.1.0-1` row;
external distribution build scripts were not executed.

Licensing is not inferred from the root file alone. `COPYING` states the MIT
transition since 1.8.0, with per-file author notices retained. Bundled GoogleTest
1.14.0 carries BSD-3-Clause grants; `INSTALL` retains its FSFULLR grant, and
`src/tools/rand48.cc` retains the Martin-Birgmeier grant (also independently
identified by the [SPDX license text](https://spdx.org/licenses/Martin-Birgmeier.html)).
Preparation copies all 325 original members with `.notice` suffixes before
generation and builds a complete SHA-256 manifest outside that directory before
moving it inside. Build and installed smoke verify every entry. The additional
packaging API driver retains its ISC grant in `PACKAGING-COPYING`.

Upstream defaults are preserved. In a fresh CMake configuration, the first
`include(CTest)` enables `BUILD_TESTING` before the later option declaration;
therefore the effective default is ON, despite that later line displaying OFF.
The recipe asserts shared libraries and tests are ON without overriding either.
It runs the entire unfiltered upstream CTest set: `index-tests` calls the seven
original geometry/RTree/MVRTree shell suites, including the million-entry RTree
bulk-load fixture, and `libsidxtest` contains 11 original GoogleTest cases.
The original TPRTree script calls are already commented out upstream; the
recipe does not change them or claim they ran. Bundled GoogleTest's own sample
and self-test options remain at their original OFF defaults; `INSTALL_GTEST`
is unset/false and no GoogleTest libraries or headers are installed.

The six additional functional API checks cover version, a C++ Point, an
in-memory index, insertion/intersection IDs/count, a disjoint query and deletion.
They assert return values and data with assertions enabled, and installed smoke
checks the post-strip driver checksum plus four C API dynamic bindings to the
installed `libspatialindex_c.so.8`. These are functional checks, not timing,
performance or native-hardware claims. The original tests and fixtures are
unchanged. The relative `lib64` CMake install directory is intentional because
upstream also uses that variable in a build-tree `export(FILE ...)` path.

The fresh official-base audit joins all 18,503 primary package records with
2,207,942 file-list rows, including exact header/library/CMake/pkg-config,
private test, documentation, license and debug namespace boundaries. It finds
no existing independent spatialindex provider or owned-path collision, and its
129-package dependency closure has 58 checked version bounds with no missing
providers. This is static official-base evidence, not an RPM solver run or
complete supplemental-repository acceptance; merge still requires exact-head
CI, actual installed products and the complete actual supplemental namespace.

The recipe requires no undeclared source fetch after materialization. The
current hosted build bridge is network-enabled and checksum-verifies cached
sources; `network_during_build=false` is not a claim of enforced offline CI.
Local validation is limited to trusted tooling and source verify-only checks:
upstream source QA, RPM/QEMU and target binaries are not executed locally.
RISC-V status remains `unknown` until exact-head target CI and physical products
are independently accepted.
