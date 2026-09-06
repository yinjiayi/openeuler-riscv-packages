# re2c

This directory packages re2c 4.5.1 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23.

The frozen discovery snapshot cross-checks the canonical component across
Arch stable Extra, Debian stable, Fedora 44, openSUSE Tumbleweed, and Ubuntu
GA. AUR offered only the VCS-only `re2c-git` derivative, so it is retained as
an excluded discovery clue rather than stable lineage. No distribution or AUR
packaging recipe was executed.

The source is the official maintainer-uploaded `re2c-4.5.1.tar.xz` release
asset. Its SHA-256 agrees with GitHub's publisher digest and an independent
download, the archive has one `re2c-4.5.1/` root with no unsafe paths or links,
and `LICENSE` explicitly places re2c in the public domain.

The RPM builds all language frontends enabled by upstream when the target's
RE2 development package is present, runs the complete upstream Automake test
suite, and exercises generated C code both during `%check` and after package
installation. Builds and tests use only checksum-pinned offline source bytes.
