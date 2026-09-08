<!-- SPDX-License-Identifier: Apache-2.0 -->
# lzlib

This directory packages the upstream `lzlib` compression library version
`1.16` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The immutable discovery snapshot identifies `lzlib` in Arch stable extra,
Debian stable, openSUSE Tumbleweed, and metadata-only AUR lineage. Ubuntu's
snapshot entry is a pre-release and is retained as rejection evidence rather
than as release evidence. The official Savannah archive is independently
reviewed, checked for safe archive members and license material, and pinned by
SHA-256. No distribution recipe or AUR content was executed.

The upstream `make check` target runs the complete maintained compression,
decompression, corruption, and API consistency test script. The package also
ships `minilzip`, the shared library, headers, Info documentation, and its man
page. CI may access the network during the build as configured by the protected
workflow; the verified source archive remains the only declared source input.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
