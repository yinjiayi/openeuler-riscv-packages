<!-- SPDX-License-Identifier: Apache-2.0 -->
# cflow

This directory packages GNU cflow `1.8` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The current stable GNU archive is immutable by digest,
SHA-256 pinned, single-rooted, free of unsafe paths and links, and contains
the upstream license and complete Autotest regression suite.

Fedora 44 GA, Debian, openSUSE Tumbleweed, Ubuntu, and read-only AUR RPC
metadata provide frozen cross-distribution lineage. No AUR PKGBUILD or
distribution recipe was read or executed. The openEuler target repository
does not contain cflow, and every declared BuildRequires is available for
the fixed target. `%check` runs the unmodified upstream `make check` target;
the installed smoke test then verifies the real parser and call-graph output
without network access.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
