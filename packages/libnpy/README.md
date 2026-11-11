<!-- SPDX-License-Identifier: Apache-2.0 -->
# libnpy

Header-only C++14 NumPy array I/O, official stable v1.0.1 at
`890ea4fcda302a580e633c624c6a63e2a5d422f6`. The fixed official archive SHA-256
is `c7b275c6cb8e46df43a20271e65010bdf63945831f2c0931ea6f2eda6a842acd`;
all 15 Git blobs were checked against the archive, with no gitlinks or symlinks.
The full MIT LICENSE and header's original notices are preserved.

The AUR discovery snapshot is historical lineage, not an executable recipe
or a stable-release authority. The official stable tag was freshly checked.
No signed release tag or detached archive signature was observed.

Upstream has no install target: install the original `npy.hpp` under
`/usr/include` and retain test sources beneath `/usr/share/libnpy`. The RPM
payload is architecture-independent; actual C++14 compilation and acceptance
remain gated on the locked openEuler 24.03 LTS SP3 riscv64/RVA23 CI image.

## Tests and target compatibility

The upstream `tests/` Meson project retains its default C++14 settings,
both original executable tests, all 15 enabled Catch cases/assertions and
the complete NumPy fixture generator. The upstream-commented unsupported bool
case remains commented; packaging neither disables nor claims that case.
`--wrap-mode=nodownload` prevents fallback downloads. Meson >= 0.55, the
existing target Catch2 v3 development package, and Python NumPy are explicit
dependencies; the source archive's v2 wrap is not fetched or vendored.

`patches/0001-catch2-v3-tests.patch` changes only the read test's v2 include
and main-provider build interface to Catch2 v3. No test body, assertion,
generator or library algorithm changes. The write test retains its own main.
The [official migration guide](https://catch2-temp.readthedocs.io/en/latest/migrate-v2-to-v3.html)
documents these header/main changes; the
[assertion reference](https://catch2-temp.readthedocs.io/en/latest/assertions.html#exceptions)
retains `REQUIRE` and string `REQUIRE_THROWS_WITH` semantics used here.
This MIT patch is downstream and not submitted upstream; remove it when the
official suite supports Catch2 v3 without it. It is dependency compatibility,
not an alleged RISC-V source defect.

`%check` executes the complete original Meson suite, then repeats it against
the staged installed header. Installed smoke checks RPM integrity and repeats
the same original suite in a fresh private directory, printing verbose test
output into the CI log before removing that private directory.
An additional downstream check loads all six original writer outputs using
NumPy with pickle disabled and compares dtype, shape and exact values.
The runner checks retained file hashes and equality to the installed header.

No local upstream/RPM/QEMU execution or target success is claimed. Source-only
verification and repository tooling validation precede submission; target
build, install, original tests and physical RPM/SRPM acceptance require CI.
This is ordinary numerical file interoperability evidence, not a hostile-file
parser security audit, performance result or native RISC-V verification.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
