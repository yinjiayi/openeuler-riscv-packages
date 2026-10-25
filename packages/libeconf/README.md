<!-- SPDX-License-Identifier: Apache-2.0 -->
# libeconf

This directory packages the official stable libeconf 0.8.4 release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The frozen 151,852-entry inventory
contains the exact `libeconf` key at 0.7.10; this package advances it to the
upstream stable [v0.8.4 release](https://github.com/openSUSE/libeconf/releases/tag/v0.8.4).
The tag resolves to immutable commit `4f951d11b1ec5dcea9fd6b4fbe192226d93050c5`.
The official commit archive was downloaded independently and its full SHA-256
matches `sources.yaml`. Its 609 tar entries have no path traversal; two test
fixture symlinks intentionally resolve to `/dev/null`.

`%check` enables `BUILD_TESTS` and runs all 45 C tests and three Bash tests
registered by upstream CTest. The optional Doxygen-generated HTML is disabled,
but upstream's shipped manual pages are installed. The installed smoke test
checks both `econftool` and the public C parsing API, and verifies that
`libeconf.pc` is installed.
No target RPM/QEMU build is claimed before the exact-head CI result is audited.

The source's `LICENSE` is MIT. Repository Apache-2.0 covers only original
packaging metadata and scripts.
