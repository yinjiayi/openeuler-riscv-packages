<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfyaml

This directory packages libfyaml `0.9.6` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. GitHub marks `v0.9.6` as the publisher's current stable
release and publishes a release asset with the same SHA-256 recorded here.
The main asset and both test-corpus archives are immutable and SHA-256 pinned.
Each has one archive root; their paths, relative in-root links, and special
members pass archive-safety inspection. Upstream `LICENSE` is MIT; GPL-2.0-only
build helpers and bundled BSD-2-Clause code are included in the source-license
expression.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` records the
component in Arch extra, Fedora 44 GA, Debian stable, openSUSE Tumbleweed, and
Ubuntu 26.04 LTS GA. Read-only AUR RPC found no exact package. No AUR or
distribution recipe was read or executed.

Upstream `configure.ac` fixes the YAML test suite at commit
`6e6c296ae9c9d2d5c4134b4b64d01b29ac19ff6f` and JSONTestSuite at commit
`d64aefb55228d9584d3e5b2433f720ea8fd00c82`. They are materialized as pinned
Source1/Source2 archives before configuration, and checkout timestamps prevent
the upstream make rules from attempting a clone. `--enable-network` only keeps
all upstream-declared corpus targets in `TESTS`; the build itself remains
network-isolated. The complete run reports 2143 total: 2139 pass, three
upstream-declared semantic skips, one expected failure, and zero fail, XPASS,
or error. No test is removed or weakened by packaging.

The openEuler 24.03 LTS SP3 RVA23 repository has no existing `libfyaml`
package or `libfyaml.so.0` provider, so `0.9.6-1` introduces no lower EVR or
SONAME replacement. The fixed dependency closure enables Check-based private
tests, libyaml compatibility, jq corpus comparisons, and both pinned corpora.
Installed smoke verifies `fy-tool`, pkg-config, and a compiled public document
API consumer.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
