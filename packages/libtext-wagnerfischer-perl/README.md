<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-wagnerfischer-perl

The frozen inventory's exact key maps to Ubuntu source 0.04-2 and official
[Text-WagnerFischer 0.04](https://metacpan.org/dist/Text-WagnerFischer) on
CPAN. The downloaded archive matches the publisher `CHECKSUMS` SHA-256
`decb05e614d0f7f85281a55e03580a100cce80dac09dc9bd77a6f59e7ed8230d`.
Its contents have one root and no traversal, links or special files. README
and module POD grant redistribution under the same terms as Perl itself;
the repository-standard dual GPL/Artistic SPDX expression records that grant.

Official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither `perl-Text-WagnerFischer` nor `perl(Text::WagnerFischer)`.
The module uses only Perl core facilities. This is a point-in-time provider
screen, not a guarantee about later repository contents.

The original default `test.pl` prints five successful checks locally, but
returns zero even if an assertion fails. `%check` retains that test and adds
fatal assertions for the same edit-distance, weighted and list behaviors.
Local source-level tests passed with Perl 5.34.1. A staging install yielded
the module and man page listed by the SPEC. Installed-RPM smoke checks the
version, provider and representative semantics. Target RPM build and install
remain CI evidence; successful PR CI alone does not prove public publication.
