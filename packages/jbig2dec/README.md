<!-- SPDX-License-Identifier: Apache-2.0 -->
# jbig2dec

This directory packages Artifex's upstream `jbig2dec` version `0.20` for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The immutable discovery snapshot records Arch stable, AUR, Debian, Fedora,
openSUSE Tumbleweed, and Ubuntu lineage for this release. The official GitHub
release archive is pinned by SHA-256 `7b63ff6470289547e7a3a0f145cb8ea6c2afffdd65645b7d87d3b7febc96fb3a`.
It contains one `jbig2dec-0.20` root directory and 75 regular files, with no
links, special files, absolute paths, or parent-directory traversal. `LICENSE`
and `COPYING` identify the project as AGPL-3.0-or-later; no release signature
was published.

The SPEC preserves libpng output support, removes only generated libtool
archives, and splits the CLI/shared library from the header, pkg-config file,
and unversioned linker name in `jbig2dec-devel`. Its `%check` runs all four
upstream targets, including the Python decoder corpus. The installed smoke
test checks the CLI version, pkg-config metadata, public version macros, and a
compiled context lifecycle against the packaged shared library. CI may access
the network while resolving dependencies and running the target build.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
