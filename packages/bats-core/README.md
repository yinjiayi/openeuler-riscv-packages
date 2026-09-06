# bats-core

This directory packages bats-core 1.14.0 as the `bats` RPM for openEuler
24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery lineage cross-checks Arch stable Extra, Debian stable,
Fedora 44, openSUSE Tumbleweed, and Ubuntu GA. The build uses only the
official upstream stable tag archive; no distribution or AUR recipe is read
or executed.

The official MIT-licensed archive is checksum pinned and contains one safe
root. Its relative test-fixture symlinks resolve within that root. `%check`
runs the complete upstream self-test directory with GNU parallel available,
and the installed smoke test executes a real TAP test.
