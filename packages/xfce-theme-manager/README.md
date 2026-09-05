<!-- SPDX-License-Identifier: Apache-2.0 -->
# xfce-theme-manager

This directory packages upstream `https://github.com/KeithDHedger/Xfce-Theme-Manager` version `0.3.9` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 2 keeps the verified source unchanged and selects its case-sensitive
`Xfce-Theme-Manager-0.3.9` top-level directory explicitly during `%prep`.
Exact-head Package CI run `33671418692` installed all BuildRequires, but the
previous default `%autosetup` directory name failed before compilation began.
No tests are skipped or weakened by this packaging-only repair.

Exact-head Package CI run `33673203229` for commit
`032fd5487979f050d0ed94fdaf8097f347e83a5c` passed `%prep` and then stopped
at the next effective configure error because `gtk+-2.0` was unavailable.
Release 3 adds openEuler's `gtk2-devel`, whose SHA-256-bound target repository
metadata provides `pkgconfig(gtk+-2.0)`; source and test execution are unchanged.

Exact-head Package CI run `33674094901` for commit
`b31ee4dd3fa30ece39c912b74679cf551df8c2ce` resolved GTK 2 and then stopped
at the next effective configure error: mandatory `libxfconf-0` was unavailable.
Release 4 declares `pkgconfig(libxfconf-0)`. The SHA-256-bound official target
metadata contains no provider and no managed provider is currently published,
so this package remains dependency-blocked; no successful build or RPM URL is
claimed.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
