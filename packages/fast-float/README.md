<!-- SPDX-License-Identifier: Apache-2.0 -->
# fast-float

This directory packages upstream `https://github.com/fastfloat/fast_float` version `8.3.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Fixed source and historical lineage

The current recipe pins these official stable tag archives in `sources.yaml`:

- [fast_float v8.3.2](https://github.com/fastfloat/fast_float/archive/refs/tags/v8.3.2.tar.gz):
  SHA-256 `71bb9e865b888df01351558db5a39586d13ea97ada162156b3a07784d8c1b26b`.
- [doctest v2.5.2](https://github.com/doctest/doctest/archive/refs/tags/v2.5.2.tar.gz):
  SHA-256 `9189960c2bbbc4f3382ce0773b2bb5f13e3afd8fed47f55f193e11e85a4f9854`.

The discovery snapshot and its distribution versions are historical lineage,
not a claim that those distributions currently ship 8.3.2. The frozen catalog's
earlier release review is not the checksum authority for this updated recipe;
the current committed source manifest is. Exact archive digests do not establish
a release signature; no signature verification is claimed.

## Test scope and evidence

The maintained C++17 unit suite runs via the unchanged `%check` / `%ctest`, with
tests enabled and the pinned doctest release supplied locally to CMake's
FetchContent. This removes the need to fetch doctest while running the suite;
it does not prove that the build container enforces network isolation.
`FASTFLOAT_SUPPLEMENTAL_TESTS` remains disabled because upstream retrieves that
optional data from the mutable `origin/main` branch rather than an immutable
release. No maintained C++17 unit target is removed. Optional exhaustive,
constexpr and C++23 suites are not covered by this recipe's acceptance claim.
The installed-RPM smoke test compiles a C++17 consumer of the installed headers
and verifies parsing `3.5`; the header-only RPM is `noarch`, while these consumer
tests execute in the locked riscv64/RVA23 target environment.

[Package CI run 38004998325, attempt 2](https://github.com/yinjiayi/openeuler-riscv-packages/actions/runs/38004998325/attempts/2)
for prior PR head `2a8bf92fd56049d0aadf0a5b6baefccfd65f2577` passed all 15
maintained C++17 tests and installed smoke. Its actual RPM/SRPM digests, headers,
source archives and SPEC were independently verified on 2026-10-10 and recorded
in the maintainer's existing `track.md`. That is evidence for the named prior
head, not this documentation revision, an arbitrary consumer, a merged main
recipe or a public RPM release. The revised PR head requires its own CI and
artifact acceptance; no download URL or publication success is inferred from
the prior CI result.
