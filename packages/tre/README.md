<!-- SPDX-License-Identifier: Apache-2.0 -->
# tre

This directory packages TRE `0.9.0` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official immutable release asset is independently
SHA-256 pinned and passed single-root, path, link, and special-entry safety
inspection. Committed snapshot
`discovery-20260808T165000Z-9a89920c269462cd` is the immutable source of the
manifest lineage and `2026-08-08T16:50:00Z` observation time. Its raw rows are
Arch `0.9.0-1`, Debian `0.9.0-1`, Fedora `0.9.0-3.fc44`, openSUSE
`0.9.0-1.7`, and Ubuntu `0.9.0-1build1`. The current official 0.9.0 source
verification is a separate hard gate, not a rewritten snapshot row.

The discovery run captured AUR metadata, but its committed canonical TRE
component contains no AUR lineage row; no PKGBUILD or distribution spec was executed. The release tarball
contains generated Autotools inputs. The build keeps NLS and agrep enabled and
adds the target's `glibc-all-langpacks` package so locale-sensitive assertions
are not silently omitted. The full upstream suite covers byte and
wide-character regular expressions, approximate matching, string-source
execution, backreferences, and agrep behavior. Installed smoke checks an
approximate CLI match and compiles a public TRE API match program.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
