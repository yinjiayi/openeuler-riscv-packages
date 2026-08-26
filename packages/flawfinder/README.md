# flawfinder

This directory packages Flawfinder 2.0.20 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Arch, Debian, Fedora, Ubuntu, and the absence of an official
openSUSE Tumbleweed package were cross-checked; no distribution or AUR recipe
is executed.

The official immutable tag archive is checksum pinned, has one safe root and
no links, and carries GPL-2.0-or-later licensing. `%check` runs all 14 upstream
golden-output tests with setuptools installed so the setup metadata test cannot
take its optional skip path.
