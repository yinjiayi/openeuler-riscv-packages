<!-- SPDX-License-Identifier: Apache-2.0 -->
# libio-dirent-perl

This directory packages upstream `https://metacpan.org/dist/IO-Dirent` version `0.05` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The CPAN archive matches the original Debian archive and the signed PAUSE
checksum entry. The author's Perl Artistic notice and the pinned full license
text are both installed.

The package builds the native XS module with RPM optimization/debug flags and
runs the original `test.pl` unchanged. Installed smoke creates a regular file
and a directory, then verifies both entry types through each XS iterator.
