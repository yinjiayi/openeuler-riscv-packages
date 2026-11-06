# Math::Fibonacci for openEuler RVA23

This package pins the official CPAN Math-Fibonacci 1.5 release at SHA-256
`70a8286e94558df99dc92f52d83e1e20a7b8f7852bcc3a1de7d9e338260b99ba`.
The publisher's `V/VI/VIPUL/CHECKSUMS` records the same digest. The frozen
Ubuntu `libmath-fibonacci-perl` 1.5-7 row supplies package lineage; it does
not substitute for the verified upstream source. Official openEuler
24.03-LTS-SP3 riscv64 RVA23 primary metadata contains neither
`perl-Math-Fibonacci` nor `perl(Math::Fibonacci)`, and provides the Perl,
POSIX, Exporter, Test and ExtUtils::MakeMaker dependencies.

The module expressly grants the included Artistic license; the Makefile and
both original test files permit the same terms as Perl. The RPM declares only
the included Artistic-1.0-Perl grant. No upstream tests or core features are
removed: `%check` runs both original `t/*.t` files and their 19 assertions.
Local source tests passed on macOS Perl 5.34.1, which is not target evidence.
The installed smoke checks the RPM/provider, module version, sequence term,
series, decomposition and membership. Target results require exact-head
hosted CI; PR artifacts do not establish public repository publication.
