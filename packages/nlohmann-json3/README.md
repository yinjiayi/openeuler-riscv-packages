<!-- SPDX-License-Identifier: Apache-2.0 -->
# nlohmann-json3

This directory packages nlohmann/json 3.12.0 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The project is header-only, so the source RPM produces the
noarch `nlohmann-json3-devel` binary package rather than an empty runtime
package. It truthfully provides the absent `nlohmann-json3` capability plus
the `json-devel`, `nlohmann-json-devel`, and `nlohmann_json-devel` names used
by Fedora, Arch-style, and openSUSE consumers. Matching static, CMake, and
pkg-config capabilities describe files actually installed by the package.

The immutable discovery snapshot combines Arch, read-only AUR metadata,
Debian, Fedora 44 GA, openSUSE Tumbleweed, and Ubuntu 26.04 LTS lineage.
Arch, Fedora, openSUSE, and the selected AUR cross-build package corroborate
3.12.0. Ubuntu's `3.12.0.really...3.11.3` string is a distribution rollback
encoding and is not interpreted as a newer upstream version. No AUR PKGBUILD
or external distribution recipe was read or executed.

The official v3.12.0 release's 114,576-byte `json.tar.xz` asset is pinned to
SHA-256 `42f6e95cad6ec532fd372391373363b62a14af6d771056dbfc86160e6dfff7aa`.
Its 69 archive members have the single `json` root, no absolute or
parent-traversal paths, no links, and no special entries. The detached
signature identifies issuer fingerprint
`797167AE41C0A6D9232E48457F3CEA63AE251B69`; the committed SHA-256 is the
mandatory CI identity and signature verification remains advisory.

The release asset intentionally contains the complete installed multi-header
tree, CMake metadata, pkg-config metadata, and license, but not the upstream
repository's external test framework or test-data checkout. `%check` therefore
does not claim the absent upstream suite: it validates bundled Hedley version
15, consumes the staged CMake package, and exercises parsing, JSON Pointer,
JSON Patch, CBOR round-trip, serialization, and non-throwing parse errors in a
compiled C++17 program. Installed smoke independently consumes the pkg-config
metadata and verifies a MessagePack round-trip.

The exact image-locked RVA23 repository metadata has SHA-256
`1e7269d6fa08e8f837e0ead13ad324e7f4ee5569dde6691378a61a806145bc14`.
It supplies CMake 3.27.9, GCC C++ 14.3.1, pkgconf 1.9.5, and
libstdc++-devel 14.3.1 for riscv64, while every checked json/nlohmann package
and capability is absent. RISC-V status remains unknown until the pinned CI
build and installed-RPM smoke test complete.

Installed nlohmann/json headers are MIT; bundled Hedley compatibility material
is additionally accounted for as CC0-1.0. Apache-2.0 covers only this
repository's original packaging metadata, tests, and documentation.
