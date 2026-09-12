<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtool

This directory packages GNU Libtool `2.6.2` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official GNU archive is independently SHA-256 pinned and
passed single-root, path, link, and special-entry safety inspection.

The frozen snapshot records Arch `2.6.2-3`, AUR Android-riscv64 `2.6.0-1`,
Debian `2.5.4-4`, Fedora 44 GA `2.5.4-10.fc44`, openSUSE Tumbleweed
`2.6.2-1.2`, and Ubuntu GA `2.5.4-9`. The AUR row is cross-target metadata
only; no PKGBUILD or distribution spec was read or executed.

The full upstream Autotest suite is a hard gate with C, C++, and Fortran
compilers installed. Static libltdl is built because the suite needs it and is
removed only after testing during package installation. Installed smoke uses
the shipped Libtool driver to compile, link, and execute a real shared library,
and calls the public libltdl API.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
