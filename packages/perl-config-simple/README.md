<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-config-simple

This directory packages Config::Simple 4.59 from the official CPAN author
archive for openEuler 24.03 LTS SP3. It is architecture-independent, while
its required package validation still runs in the riscv64/RVA23 target.

The frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd`
cross-checks Arch Extra 4.59-20, Fedora 44 4.59-50.fc44, Debian stable
4.59-7, and openSUSE 4.59-19.37. The snapshot's AUR records are retained
only as read-only supplemental discovery lineage and are not treated as
Config::Simple source identity; no PKGBUILD or distribution recipe was read
or executed.

The official CPAN archive is SHA-256 pinned and contains its MakeMaker build
plus all ten upstream test files. `make test` runs the complete 89-test
parser, writer, syntax-guessing, import, tie, modification, and regression
suite without exclusions.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts,
and documentation in this directory.
