<!-- SPDX-License-Identifier: Apache-2.0 -->
# miniz

This directory packages upstream `https://github.com/richgel999/miniz`
version `3.1.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch Extra
`3.1.2-1`, the AUR metadata-only `mingw-w64-miniz` entry `3.1.2-1`, Fedora
44 `3.1.1-1.fc44`, and openSUSE Tumbleweed `3.1.2-1.3`. No AUR recipe or
distribution build script was read as executable content or executed.

GitHub identifies `3.1.2` as the current stable release. The official
release-tag archive is pinned at SHA-256
`98468f8924934b723276680f85238b6c78bf1f8b49b4459cc9b7214a20e2e9fb`;
it is a single-root archive with no unsafe paths, links, or special files.
Unlike the reduced amalgamated release asset, it retains the complete
registered Catch2 suite. `%check` runs that suite and all six shipped example
programs offline. The separate developer stress script that downloads a Linux
kernel tree is not a registered release test target and is incompatible with
the repository's no-network build policy.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
