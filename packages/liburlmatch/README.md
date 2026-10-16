<!-- SPDX-License-Identifier: Apache-2.0 -->
# liburlmatch

This directory packages upstream `https://github.com/clbr/urlmatch` version `1.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The official `v1.0` tag resolves to `24f72a0ea15402d28143fc84ca60b13f3dd033a7`.
The fixed official archive has SHA-256
`61ae069198c111dfad86fea42ff07ed3b9454cefa51657f78a9f26abfc5dce35`;
all 25 regular source files were compared with their Git blobs. Library notices
grant AGPL version 3 only (`AGPL-3.0-only`); complete `COPYING` and original
notices are retained. No source patches or external distribution recipes are used.

Upstream produces only `liburlmatch.a` and `urlmatch.h`. The canonical
development package provides `liburlmatch-devel` and `liburlmatch-static`, with
the archive relocated from upstream's fixed `/usr/lib` to target `/usr/lib64`.
It does not claim a shared ABI or install an invented command-line interface.
The target official and supplemental metadata were checked for these three RPM
names, the header/archive paths, and all 15 build dependency roots; no name/path
collision or missing root was found. Metadata coverage is not a completed DNF
transaction or a successful target build.

`make test` is preserved with the original eight programs: `allocfree`, `bin`,
`count`, `opti`, `rated`, `shortrule`, `simple`, and `str`. A trailing `LDLIBS=-lz`
keeps zlib after objects under linkers using `--as-needed`. Upstream's original
test runner can report failures while returning success, so `%check` also
requires the exact eight-program membership and checks each executable's exit
code directly. Assertions remain enabled. The installed replay preserves and
checksums all original test sources, harness and necessary internal headers;
it compiles those unchanged sources against the installed public header and
static archive, then requires all eight exits. These are repeated executions of
eight original programs, not additional unique tests. The compiler and zlib
development requirements support that installed development contract.

Local verification is limited to trusted packaging-tool tests, shell syntax,
fixed-source integrity and inert recipe inspection. No upstream program, RPM or
QEMU build is executed locally. Hosted target CI, genuine install logs and
independently inspected RPM/SRPM bytes remain required for acceptance. The
separate upstream benchmark is not the default test target, and no native
performance or RVA23 hardware result is claimed.
