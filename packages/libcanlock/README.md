<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcanlock

This directory packages libcanlock 3.3.3 for openEuler 24.03 LTS SP3
`riscv64`/RVA23. The [official project announcement](https://micha.freeshell.org/libcanlock/)
dates the 3.3.3 release to 2026-07-07. Its [official source index](https://micha.freeshell.org/libcanlock/src/info.html)
lists the 638,066-byte archive and SHA-256
`6a05291c4ca12169287d78f9e6d083c85b4eb180ceeb16403924e4310b681651`;
the independently downloaded HTTPS archive matches both. All archive paths
remain under `libcanlock-3.3.3/`, and its three symbolic links target files
inside that root.

The upstream `COPYING` identifies BSD-3-Clause and ICU for code and manual
pages, and NLPL for README and ChangeLog. GNU Autotools files carry their own
ancillary licenses. The package retains the default legacy API and header
parser subproject. `%check` runs the complete recursive upstream `make check`:
five root tests and thirteen header-parser tests, including two upstream-declared
expected failures. One header-parser library test is upstream-marked to skip
until installation; the installed smoke test separately exercises that API.
Expected failures are reported as XFAIL, not claimed as passing assertions.
Static archives are built for the upstream SHA test and
removed from the installed RPM. The installed smoke test compiles and runs a
public C API roundtrip against both installed shared libraries and checks both
pkg-config files and three command-line tools. Target-architecture results
remain unverified until the PR CI completes.
