<!-- SPDX-License-Identifier: Apache-2.0 -->
# jo

This directory packages jo `1.9` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The publisher's current stable release asset is SHA-256
pinned, single-rooted, and free of unsafe paths, links, and special members.
The command is GPL-2.0-or-later, its JSON helper is MIT, and its base64 helper
is dedicated to the public domain.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` records jo in
Arch extra, Fedora 44 GA, Debian stable, openSUSE Tumbleweed, and Ubuntu
26.04 LTS GA. Read-only AUR RPC found no exact `jo` package. No AUR
PKGBUILD or distribution recipe was read or executed.

The fixed openEuler RVA23 repository has no existing `jo` package, and jo
installs no shared library. `%check` runs all 27 upstream TAP cases covering
objects, arrays, nested data, files, pipes, stdin, coercion, filtering,
overwrites, and errors; the observed summary had 27 passes and zero skips,
XFAILs, failures, XPASSes, or errors. Installed smoke produces and checks a
real typed JSON object.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
