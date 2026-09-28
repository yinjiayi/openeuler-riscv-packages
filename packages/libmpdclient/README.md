<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmpdclient

This directory packages libmpdclient 2.26 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official Music Player Daemon release archive is fetched
over HTTPS and verified against the SHA-256 in `sources.yaml` before RPM build.
Its 150 archive entries contain only ordinary files and directories under the
`libmpdclient-2.26/` root. Both BSD-2-Clause and BSD-3-Clause license texts
are included.

The frozen discovery snapshot records libmpdclient 2.26 in Arch extra and
openSUSE Tumbleweed, and older versions in Debian stable and Ubuntu. The
upstream build uses Meson with its complete two-test suite enabled. The
installed smoke test queries package and pkg-config versions, links a small C
consumer, and exercises public tag-parsing functions without an MPD server.

The publisher released 2.27 after this selected 2.26 package version; the
update checker should propose a separate version update. Target build and
installation status remain unknown until CI passes on the pinned openEuler
RISC-V image. External source licenses govern upstream code; this repository's
Apache-2.0 license covers its original packaging metadata and scripts.
