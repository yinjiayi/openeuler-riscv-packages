<!-- SPDX-License-Identifier: Apache-2.0 -->
# datamash

This directory packages GNU datamash `1.9` for openEuler 24.03 LTS SP3
on `riscv64`/RVA23. The current stable GNU archive is immutable by digest,
SHA-256 pinned, single-rooted, free of unsafe paths and links, and includes
the upstream license plus its maintained regression suites.

Arch stable, Fedora 44 GA, Debian, openSUSE Tumbleweed, and Ubuntu provide
frozen cross-distribution lineage. AUR was queried through read-only RPC and
had no matching package; no AUR PKGBUILD or distribution recipe was read or
executed. The fixed openEuler target supplies all declared dependencies,
including Valgrind and locale data. `%check` runs upstream `check-expensive`,
which includes the normal suite, expensive I/O tests, Valgrind checks, and
the German-locale coverage without test exclusions. Installed smoke verifies
both tabular aggregation and the `decorate` Roman-numeral sorting path.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
