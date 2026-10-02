<!-- SPDX-License-Identifier: Apache-2.0 -->
# Class::Field 0.24

The frozen `libclass-field-perl`/`perl-Class-Field` inventory lineage includes
Debian source `libclass-field-perl` 0.24-2 and Fedora 0.24-21.fc44. The
official stable CPAN archive is 12,972 bytes; its SHA-256
`233064e094442f2e449844da9aec9ce0e0ed65a7da7abdb25ec0dc1be454df98`
matches publisher INGY `CHECKSUMS`.

The top-level `LICENSE` explicitly grants same-as-Perl redistribution for
this software. Installed `lib/Class/Field.pod` and README repeat the grant;
the implementation, four functional tests, author-only POD test and generated
build metadata have no contrary notices or vendored code. The RPM license
expression records the GPL-1-or-later or Artistic-1 choice.

Official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Class-Field` name or `perl(Class::Field)` provider. It supplies
`perl(Encode)` 3.21, `perl(Data::Dumper)` 2.183, `perl(Scalar::Util)` 1.63,
`perl(Test::More)` 1.302198, `perl(File::Find)` 1.43 and MakeMaker 7.70.
The unmodified default suite has four functional files/15 assertions;
`t/author-pod-syntax.t` is retained but self-skips without `AUTHOR_TESTING`.
Local original tests passed 15 assertions with two taint-mode warnings that
did not affect results. Target CI must prove all four functional files, all
15 assertions, the expected author-only skip, physical RPM/SRPM products,
DNF installation and installed field/const smoke. No local RPM or QEMU build
was run, and a PR build is not publication.
