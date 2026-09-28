<!-- SPDX-License-Identifier: Apache-2.0 -->
# libxcvt

This package maps the inventory's exact `libxcvt` key to X.Org's official
stable 0.1.3 release for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The
[X.Org announcement](https://lists.x.org/archives/xorg-announce/2024-December/003571.html)
publishes SHA-256 `a929998a8767de7dfa36d6da4751cdbeef34ed630714f2f4a767b351f2442e01`
for the HTTPS tarball, matching the independently downloaded archive. The
archive has one top-level source tree without traversal paths, links, or
special files. CI fetches and verifies the pinned hash before building.

The upstream Meson project registers no test cases. `%check` retains
`%meson_test` without claiming an upstream functional suite. The installed
smoke runs the public `cvt` CLI on the upstream README's 1920x1200 at 75 Hz
example, then compiles, links, and runs a client of the public C modeline API.
These checks require no X server but do not cover every mode-line input.

Upstream `COPYING` contains MIT and HPND-sell-variant notices, both recorded
in the RPM license expression. The main package installs the shared library,
`cvt` tool, and manual; devel installs headers and pkg-config metadata. CI
artifacts are not evidence of public RPM repository publication.
