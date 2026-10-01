# universal-ctags

This directory packages Universal Ctags 6.2.1 for openEuler 24.03 LTS SP3
on `riscv64`/RVA23. Arch Extra, Debian stable, Fedora 44, openSUSE
Tumbleweed, and Ubuntu GA aliases are deduplicated to the official ctags.io
component. No distribution or AUR packaging content is executed.

The official maintainer release asset and publisher SHA-256 are pinned. The
archive has one safe root and GPL-2.0 license text. All target-supported JSON,
XML, YAML, PCRE2, and seccomp features are enabled. `%check` runs upstream's
complete `make check` route without removing tests or converting failures to
skips.
