<!-- SPDX-License-Identifier: Apache-2.0 -->
# less

This directory packages less `704`, the upstream site's current recommended
general-use release, for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The
official archive is independently SHA-256 pinned and passed single-root, path,
link, and special-entry safety inspection.

The frozen snapshot records Arch `1:704-1`, Debian `668-1`, Fedora 44 GA
`691-2.fc44`, openSUSE Tumbleweed `704-1.3`, and Ubuntu GA `668-1build1`; it
contains no canonical stable AUR row. No AUR recipe or distribution spec was
read or executed. This package contains only upstream less, not Fedora's
secondary lesspipe source. Its complete bundled `make test`/lesstest suite is a
hard gate with no ignored failures. Installed smoke performs noninteractive
paging on real text.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
