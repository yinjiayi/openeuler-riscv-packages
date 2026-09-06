# cppcheck

This directory packages Cppcheck 2.21.1 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Arch Extra, Debian stable, Fedora 44, openSUSE Tumbleweed,
and Ubuntu GA aliases are deduplicated to the official Cppcheck component.
No distribution or AUR packaging content is executed.

The immutable official tag archive is checksum pinned, contains one safe
archive root, and carries GPL-3.0-or-later licensing. The build enables the
upstream rules engine and match compiler. `%check` runs the complete unit,
configuration, platform, CWE, and XML validation gates without suppressing
failures or converting failures to skips.
