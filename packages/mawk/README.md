<!-- SPDX-License-Identifier: Apache-2.0 -->
# mawk

This directory packages mawk `1:1.3.4.20260302-1` for openEuler 24.03 LTS
SP3 on `riscv64`/RVA23. The publisher's current archive and manual identify
stable release `1.3.4` dated `20260302`. The official archive is SHA-256
pinned, has one root, and contains no unsafe path, link, or special member.
Source notices and `COPYING` establish GPL-2.0-only.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` records mawk
in AUR metadata, Fedora 44 GA, Debian stable, openSUSE Tumbleweed, and Ubuntu
26.04 LTS GA. Read-only AUR RPC reports `1.3.4_20260302-1`. No AUR or
distribution recipe was read or executed. Epoch `1` preserves the established
Fedora package epoch rather than introducing a lower cross-lineage EVR.

The openEuler 24.03 LTS SP3 RVA23 repository has no existing `mawk` package;
mawk installs no shared library, so there is no SONAME replacement. The fixed
test closure explicitly includes POSIX shell, core utilities, `cmp`, `grep`,
and `sed`. `%check` runs all three official targets: `mawk_test`, `mawk_errs`,
and `fpe_test`, without a downstream exclusion. Installed smoke verifies the
exact version and an AWK aggregation.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
