<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcyaml

This directory packages upstream `https://github.com/tlsa/libcyaml` version
`1.4.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch stable
`extra` (`1.4.2-1`), the AUR metadata-only `libcyaml-git` entry
(`1.3.0+r630.5206ece-1`), Fedora 44 (`1.4.2-4.fc44`), Debian stable
(`1.4.2-1`), and Ubuntu Resolute GA (`1.4.2-1build1`). The same snapshot was
queried for openSUSE Tumbleweed `oss` and contained no `libcyaml` source
component; that negative result is recorded here rather than inventing a
lineage row. No AUR recipe or distribution build script was read or executed.

The full upstream test gate means the complete schema, load, save, error,
file, UTF-8, free, and utility unit suite runs twice: once against the shared
library and once against the static library. The suite and fixtures are fully
contained in the official release archive and require no network access or
third-party test framework.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
