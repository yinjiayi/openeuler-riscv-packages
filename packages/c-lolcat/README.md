<!-- SPDX-License-Identifier: Apache-2.0 -->
# c-lolcat

This directory packages upstream `https://github.com/jaseg/lolcat` version `1.5` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The source is the official stable v1.5 commit
`a9ab81839f2a00fa1d831648a1d79e268bb1ddac`, not the stale AUR 1.4 snapshot.
Source0 SHA-256: `97860debda5631417df11dc7dd617af969e740eeffd9b41e4aa228d303aa48bc`.
Both original default tools (`lolcat` and `censor`) use the original root
`make all` and `make install` targets; optional autotools packaging is not used.

The sole zero-context patch selects `python3` instead of `python` for the
unchanged f-string table generator. The full original Makefile hash is required
before patching. Target CI regenerates the table and must reproduce the original
header SHA-256 `7e0d41fdaa9558663fb333fd825c2aa95b2b40afca8562ff018154d8f971b332`.
No color algorithm, default feature, source notice or original test is removed.

There is no upstream check/test target. “Downstream CLI smoke” means the separate
16 behavior checks embedded in %check and repeated after RPM installation:
non-TTY ASCII/Unicode copy, version/help, forced 256/16/RGB/gradient color,
multiple files/stdin, missing files, invalid arguments and censor/ANSI behavior.
Both tools must be physical RISC-V ELF files, with unchanged hashes; installed
files must be owned by this RPM. All 17 original source files, Source0 and notices
are preserved and checked. This is not an upstream test suite, native/interactive
TTY validation or a performance claim. Target build/install results remain
unverified until exact-head CI and physical products are checked.

The generator states it was copied from Pygments. In addition to original WTFPL
notices, the package conservatively retains the complete official BSD-2-Clause
LICENSE, AUTHORS and RGB-to-XTERM attribution from Pygments stable 2.19.2 commit
`cfca62e6e95136e48a255e8cbffb0bbe1d98456c`. That notice provenance does not assert
the historical copied Pygments version. License: `WTFPL AND BSD-2-Clause`.
Python is generator/test support, not an added runtime requirement.

Canonical admission checks cover official/supplemental primary and filelists,
all current open PR package metadata, and both command paths. Data::Censor's Perl
PR is a different component, not the C censor command. Dependency metadata is
an admission check, not proof of a successful DNF transaction; CI must resolve
the actual build/test tools.

External source and patch licenses remain those of their respective upstream
projects. The repository license only covers original packaging metadata,
scripts, and documentation.
