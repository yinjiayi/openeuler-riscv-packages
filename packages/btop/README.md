<!-- SPDX-License-Identifier: Apache-2.0 -->
# btop

This directory packages the official `https://github.com/aristocratos/btop`
release `1.4.7` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The GitHub
tag archive is pinned by SHA-256 `933de2e4d1b2211a638be463eb6e8616891bfba73aef5d38060bd8319baeefc6`
in `sources.yaml`; the reviewed archive has one `btop-1.4.7/` root and no
absolute paths, parent traversal, or symlinks.

The frozen discovery snapshot in `package.yaml` cross-checks Arch stable,
Debian stable, Fedora 44, and openSUSE Tumbleweed. Distribution metadata is
lineage evidence only; no distribution recipe or AUR `PKGBUILD` was executed.
The upstream Apache-2.0 license remains applicable to the source, while the
repository license covers only original packaging metadata and tests.

The SPEC uses the upstream Linux Makefile with the target compiler flags and
explicit `riscv64` platform. The Makefile's bundled fmt headers and Linux
collector require only GCC C++, GNU Make, and the standard C++23 library;
RISC-V builds do not enable the x86-specific Intel/ROCm GPU path. The install
stage preserves the upstream binary, themes, desktop entry, icons, and README.
`%check` and installed smoke verify version/help/default-config output and all
installed desktop/theme assets without starting an interactive terminal UI.
