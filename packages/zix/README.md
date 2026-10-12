<!-- SPDX-License-Identifier: Apache-2.0 -->
# zix

This directory packages upstream `https://gitlab.com/drobilla/zix` version
`0.8.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch stable
`extra` (`0.8.2-1`), the AUR metadata-only `zix-git` entry
(`1:0.8.1.r642.e1cbd66-2`), Fedora 44 (`0.8.0-2.fc44`), openSUSE Tumbleweed
(`0.8.0-1.5`), Debian stable (`0.6.2-1`), and Ubuntu Resolute GA
(`0.8.0-1`). No AUR recipe or distribution build script was read or executed.

The full upstream test gate means every shipped C unit test, expected-failure
case, threaded test, public C-header check, and C++17 comparison test is built
and run. Platform checks and POSIX/thread support are explicitly enabled;
documentation, lint, and benchmarks are not test targets and remain disabled.
The official release archive is SHA-256 pinned and Meson is forced to remain
offline.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
