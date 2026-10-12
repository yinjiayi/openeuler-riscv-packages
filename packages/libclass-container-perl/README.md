<!-- SPDX-License-Identifier: Apache-2.0 -->
# Class::Container 0.13

The frozen `libclass-container-perl`/`perl-Class-Container` inventory lineage
includes Debian source `libclass-container-perl` 0.13-2, Fedora 0.13-24.fc44
and openSUSE 0.13. The official stable CPAN archive is 25,768 bytes; its
SHA-256 `f5d495b1dfb826d5c0c45d03b4d0e6b6047cbb06cdbf6be15fd4dc902aeeb70b`
matches the KWILLIAMS publisher `CHECKSUMS` entry.

The top-level `LICENSE` explicitly grants same-as-Perl redistribution for
this software. The installed `lib/Class/Container.pm` repeats the grant and
credits Ken Williams and Dave Rolsky for original HTML::Mason work. Tests,
fixtures and generated build metadata have no conflicting notice or vendored
code. The RPM license expression records the GPL-1-or-later or Artistic-1
choice.

Official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Class-Container` name or `perl(Class::Container)` provider. It provides
`perl(Params::Validate)` 1.31, `perl(Module::Build)` 0.4234, and the other
upstream build/runtime prerequisites. The unmodified default suite has two
functional files/92 assertions. `t/author-critic.t` is present and self-skips
unless `AUTHOR_TESTING`; it is not a functional skip. A local run passed all
92 assertions and printed two taint-mode `require` warnings from the original
tests. Target CI must prove the same functional coverage, physical RPM/SRPM
artifacts, DNF installation and installed containment smoke. No local RPM or
QEMU build was run; a PR build is not publication.
