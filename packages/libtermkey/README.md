<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtermkey

This directory packages libtermkey `0.22` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official upstream `v0.22` tag resolves to immutable
commit `c97f926ddcd1ade551162272bd4c8cf69e0b7de2`; that commit archive is SHA-256 pinned,
single-rooted, and free of unsafe paths, links, or special members. It contains
the upstream MIT license and all maintained TAP tests.

Read-only AUR RPC metadata, Debian, Fedora 44 GA, openSUSE Tumbleweed, and
Ubuntu provide frozen cross-distribution lineage. No AUR PKGBUILD or
distribution recipe was read or executed. The package is new to the fixed
target repository; its audited BuildRequires use the immutable supplemental
repository's reviewed `unibilium-devel` package and introduce upstream's
stable `libtermkey.so.1` ABI.

`%check` runs upstream `make test`, which builds all 17 maintained C test
programs and executes them through the strict TAP `prove` runner without
exclusions. Installed smoke verifies the SONAME and compiles against the
public push-bytes, parse, and format APIs without a terminal or network.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
