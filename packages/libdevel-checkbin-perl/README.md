<!-- SPDX-License-Identifier: Apache-2.0 -->
# Devel::CheckBin 0.04

The frozen Ubuntu `libdevel-checkbin-perl` 0.04-3 inventory key maps to
official stable [Devel-CheckBin 0.04](https://metacpan.org/dist/Devel-CheckBin).
Publisher CHECKSUMS and the independently downloaded 9,866-byte HTTPS archive
agree on SHA-256
`157f3db59c29ed1d49133a469cee772c885ad4ee64e8692a91b3ebfdbe2fe3e4`.
The archive has one top-level tree, regular files and no vendored code.

The installed `lib/Devel/CheckBin.pm`, README and bundled LICENSE explicitly
grant same-as-Perl redistribution by tokuhirom, with no conflicting notice in
the three default test files. The RPM license expression records Perl's GPL
version 1-or-later or Artistic choice.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Devel-CheckBin` package or module provider. It supplies EUMM 7.70,
Test::More 1.302198, File::Temp, File::Spec, Config, Exporter, parent,
and coreutils containing `/usr/bin/ls`. The three unchanged default tests
locally passed five top-level assertions and both nested t/02 branches with
no skips. Target CI must prove the same full suite, physical RPM/SRPM, DNF
installation and installed positive/negative command lookup. Upstream
`check_bin` deliberately exits zero when a command is missing; this behavior
is retained, and the original test checks its diagnostic output rather than
its exit code. No local RPM or QEMU build was run, and PR CI is not repository
publication.
