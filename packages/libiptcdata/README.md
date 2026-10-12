<!-- SPDX-License-Identifier: Apache-2.0 -->
# libiptcdata

The official `release_1_0_5` GitHub release provides libiptcdata 1.0.5.
Its HTTPS release archive has SHA-256
`c094d0df4595520f194f6f47b13c7652b7ecd67284ac27ab5f219bc3985ea29e`
and contains only regular files and directories under one source root. Source
headers license the library LGPL-2.0-or-later; `COPYING` contains the GNU
Library General Public License version 2. Fedora metadata is discovery
lineage only and no distribution recipe was read or executed.

This package targets openEuler 24.03 LTS SP3 on `riscv64`/RVA23. It includes
the shared C library, public headers, pkg-config metadata, translations,
upstream gtk-doc pages, and the `iptc` command. Optional Python bindings are
outside the initial package scope; they are not a core library feature.

The upstream archive has no registered library test program. `%check` runs its
`make check` target, checks the CLI version and tag list, and verifies an IPTC
caption can be serialized and parsed back through the library API. Installed
RPM smoke repeats the API round trip and CLI version check. This functional
test does not claim exhaustive JPEG parser coverage. New upstream releases
must be reviewed because the asset tag embeds the version with underscores.
The first CI build at head `28c4f30899d5ae7674ff7562bc43711b2fc8e83e`
failed solely at RPM file accounting: upstream installed generated gtk-doc
pages despite `--disable-gtk-doc`. Those pages are now owned by the devel RPM;
build and smoke still require a new exact-head CI run.

Apache-2.0 covers the original packaging metadata, test, and documentation
here; the upstream library retains LGPL-2.0-or-later terms.
