<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-six

This directory packages Six 1.17.0 for openEuler 24.03 LTS SP3. The package
is architecture-independent; its required validation still runs in the
riscv64/RVA23 target.

The frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd`
cross-checks Arch Extra 1.17.0-3, AUR metadata for pypy3-six 1.17.0-1,
Fedora 44 1.17.0-8.fc44, Debian stable 1.17.0-1, openSUSE 1.17.0-1.7,
and Ubuntu Resolute 1.17.0-2build1. No AUR PKGBUILD or distribution recipe
was read or executed.

The source URL pins the official 1.17.0 tag's resolved full commit. The
SHA-256-pinned archive contains the complete upstream pytest suite.
`python3 -m pytest -v` runs all compatibility, moved-module, metaclass,
exception, iterator, text, and byte tests; tkinter is an explicit fixed
BuildRequires so those import checks are not silently omitted.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts,
and documentation in this directory.
