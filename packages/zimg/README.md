# zimg

This directory packages zimg 3.0.6 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23.

The frozen discovery snapshot cross-checks the canonical component across
Arch stable Extra, an AUR metadata-only derivative, Debian stable, Fedora 44,
and openSUSE Tumbleweed. No distribution or AUR recipe was executed.

The primary archive is generated from the official immutable `release-3.0.6`
tag and is SHA-256 pinned. Upstream's unit-test tree references GoogleTest at
the exact gitlink commit `703bd9caab50b139428cea1aaff9974ebee5742e`;
that official dependency archive is independently pinned and materialized
offline. Both archives have safe paths. zimg carries WTFPL terms in `COPYING`;
the test dependency carries its own BSD-style license.

The RPM bootstraps the official Autotools build, enables the complete upstream
unit test binary, runs `make check`, and compiles an installed C API version
probe. No source, submodule, or dependency is fetched during build or tests.
