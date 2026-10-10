<!-- SPDX-License-Identifier: Apache-2.0 -->
# gengetopt

This directory packages GNU gengetopt version `2.23` for openEuler 24.03 LTS
SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch stable
`extra` (`2.23-4`), Fedora 44 (`2.23-17.fc44`), openSUSE Tumbleweed
(`2.23-1.26`), Debian stable (`2.23+dfsg1-1`), and Ubuntu Resolute GA
(`2.23+dfsg1-1build1`). The AUR metadata-only `gengetopt-git` entry was also
checked, but its last update was 2023-04-10, more than 24 months before this
snapshot, so policy excludes it from discovery lineage. No AUR recipe or
distribution build script was read or executed.

The full upstream test gate is the release tarball's serial `make check`
Automake suite. It builds and runs the complete generated-parser matrix,
configuration-file cases, expected errors, output-directory behavior, help
output, groups, modes, multiple parsers, named and unnamed arguments, and
value handling. Upstream documents that its parallel build is unsafe, so both
the build and test phases are intentionally serial rather than weakening or
skipping any tests.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
