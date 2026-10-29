# Algorithm::LUHN 1.02

Official source: `https://cpan.metacpan.org/authors/id/N/NE/NEILB/Algorithm-LUHN-1.02.tar.gz`.
The publisher `CHECKSUMS` in that directory records SHA-256
`e808fbba13e262608d37923efa917e18407453c4af96ab783fc77f9fe159b9c0`.
The archive contains only regular files and directories under one root, with
no patches.

The official `LICENSE`, README and module POD identify Tim Ayers as copyright
holder and grant redistribution under the same terms as Perl itself. The RPM
uses `GPL-1.0-or-later OR Artistic-1.0-Perl` and installs the license text.

The official SP3 RVA23 primary has no `perl-Algorithm-LUHN` name or
`perl(Algorithm::LUHN)` provider. It supplies Perl 5.38 and the required
Exporter, ExtUtils::MakeMaker and Test modules. The unmodified local default
`make test` passes all three files and 48 assertions without skips on Perl
5.34.1. `%check` retains the complete upstream default suite; target build,
install and smoke require separate exact-head hosted CI evidence.

The frozen 151,852-row inventory records Fedora `1.02-30.fc44` lineage; that
row is not source, licensing, dependency or target-build proof.
