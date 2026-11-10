<!-- SPDX-License-Identifier: Apache-2.0 -->
# Text::Reflow 1.17

This package installs the Perl XS module (a compiled Perl extension), the
`reflow` command, and their manual pages for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The fixed CPAN archive matches both MetaCPAN and its
publisher's CHECKSUMS file.

The original module notice offers GPL-3.0-or-later as a choice. The
distribution's module and compiled extension are packaged under that grant;
the separate command retains its own GPL-2.0-or-later notice. The package
retains both original notices and carries complete checksum-pinned GNU GPL
v2 and v3 texts.

The recipe runs the original `make test` unchanged. Its 20 original assertions
and the staged extension/CLI smoke passed on the macOS host. That does not
verify the openEuler Perl ABI or RISC-V RPM build and installation; exact target
CI supplies that evidence.
