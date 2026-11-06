# Math::VecStat for openEuler RVA23

This package pins official CPAN Math-VecStat 0.08 at SHA-256
`409a8e0e4b1025c8e80f628f65a9778aa77ab285161406ca4a6c097b13656d0d`,
matching the publisher's `A/AS/ASPINELLI/CHECKSUMS`. Frozen Ubuntu
`libmath-vecstat-perl` 0.08-3 supplies package lineage, not source trust.
Official openEuler 24.03-LTS-SP3 riscv64 RVA23 primary metadata has neither
`perl-Math-VecStat` nor `perl(Math::VecStat)` and supplies core Perl, Exporter,
and ExtUtils::MakeMaker.

The upstream README names both copyright holders and grants redistribution of
the program under the same terms as Perl. The module, Makefile and original
test have no contrary notices. The RPM installs that README as license
evidence and declares the corresponding GPL-1.0-or-later or
Artistic-1.0-Perl choice. No upstream tests or features are removed:
`%check` runs the sole original `t/VecStat.t` with all 40 assertions.
Local source tests passed on macOS Perl 5.34.1, not the target system.
Installed smoke checks the RPM/provider, version, min, max, sum, average,
median and vector product. Target validation requires exact-head hosted CI;
PR artifacts do not establish public repository publication.
