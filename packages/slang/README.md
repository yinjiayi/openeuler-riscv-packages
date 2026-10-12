<!-- SPDX-License-Identifier: Apache-2.0 -->
# slang

This directory packages S-Lang `2.3.3` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The current stable publisher archive is immutable by version,
SHA-256 pinned, single-rooted, and free of unsafe paths, links, and special
members. Its source headers license S-Lang under GPL-2.0-or-later.

Arch stable, Debian, Fedora 44 GA, openSUSE Tumbleweed, and Ubuntu provide
frozen cross-distribution lineage. The frozen AUR alias result belongs to the
unrelated `jed` package, so it is deliberately excluded rather than treated as
S-Lang evidence. No AUR RPC content or distribution packaging recipe is read
or executed. Release `4` supersedes the fixed target's `2.3.3-3` while
preserving the main/devel/help split and `libslang.so.2` ABI required by
existing target consumers.

The complete upstream `make check` gate is mandatory. It runs the interpreter
and C API corpus in normal and UTF-8 modes, every configured module test, and
all slsh library tests. PCRE, Oniguruma, PNG, zlib, iconv, and sysconf modules
remain enabled so their conditional tests run. `TERM=xterm` supplies the
terminal capabilities required by the upstream screen-module test; no test is
excluded or converted to a skip. Installed smoke exercises slsh, verifies the
SONAME capability, and compiles and runs a public C API program without
network access.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
