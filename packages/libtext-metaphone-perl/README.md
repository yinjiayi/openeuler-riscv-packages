<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-metaphone-perl

The frozen inventory's exact key maps to Ubuntu source 20160805-2build5 and
official [Text-Metaphone 20160805](https://metacpan.org/dist/Text-Metaphone)
on CPAN. The downloaded archive matches publisher `CHECKSUMS` SHA-256
`2d07e7cdafdf8f8f2b2698c0163f40018ca2d20e064a465c18161d581a405a41`.
It has one root without traversal, links or special files. Distribution
metadata and module POD grant redistribution under the same terms as Perl;
the C, XS and header files carry no separate conflicting notice. The module
POD describes the C algorithm's public-domain predecessor, which is not a
claim that this distribution itself is public domain.

Official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither `perl-Text-Metaphone` nor `perl(Text::Metaphone)`.
It has `gcc`, `perl-devel`, ExtUtils::MakeMaker and Test::More. This is a
point-in-time provider screen, not a future guarantee.

The complete original `t/metaphone.t` suite passed all 22 assertions in a
scratch source build with Apple clang and Perl 5.34.1; that host build is not
evidence for the target RISC-V ABI. A staging install yielded an
architecture-dependent module, shared library and man page, which are listed
by the SPEC. Target CI must prove the riscv64 RPM build, binary load, RPM
dependency header and installation/smoke. Successful PR CI alone does not
prove public RPM repository publication.
