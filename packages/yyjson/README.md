<!-- SPDX-License-Identifier: Apache-2.0 -->
# yyjson

yyjson 0.12.0 for openEuler 24.03 LTS SP3 `riscv64`/RVA23. The
official stable tag archive is SHA-256 pinned and inspected for safe paths,
links, and the MIT license. Frozen lineage cross-checks Arch extra, Debian
stable, Fedora 44 GA, and openSUSE Tumbleweed. No distribution script was read
or executed. Every upstream C/C++ test is enabled. The installed smoke test
uses Python `ctypes` to load the packaged shared library and perform a JSON
parse/serialize round trip, so it does not assume a compiler is present in the
runtime image. Apache-2.0 covers packaging material only.
