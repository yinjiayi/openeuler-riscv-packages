<!-- SPDX-License-Identifier: Apache-2.0 -->
# iniparser

This directory packages upstream `https://gitlab.com/iniparser/iniparser`
version `4.2.6` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch stable
`extra` (`4.2.6-2`), the AUR metadata-only `iniparser-git` entry
(`1:4.2.6-1`), Fedora 44 (`4.2.6-4.fc44`), openSUSE Tumbleweed
(`4.2.6-2.2`), Debian stable (`4.2.6-1`), and Ubuntu Resolute GA
(`4.2.6-1build1`). No AUR recipe or distribution build script was read or
executed.

The full upstream test gate means both shipped Unity suites—dictionary and INI
parser behavior, including all bundled malformed, quoted, UTF-8, and legacy
fixtures—run through CTest. Upstream normally fetches an unpinned Unity branch
during configuration, so this package supplies the official Unity `v2.7.0`
release as a separately SHA-256-pinned test source and forces FetchContent into
fully disconnected mode. Because that source override bypasses FetchContent's
patch step, `%prep` reproduces upstream's declared copy of `unity_config.h`
into the pinned Unity tree. Unity is used only to build tests and is not
shipped.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
