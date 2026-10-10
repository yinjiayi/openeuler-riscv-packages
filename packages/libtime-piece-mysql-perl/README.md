# Time::Piece::MySQL 0.06

The frozen 2026-08-08 inventory includes Fedora Everything-source
`perl-Time-Piece-MySQL` 0.06-29.fc44 and Ubuntu resolute/universe
`libtime-piece-mysql-perl` 0.06-3. This package uses the official KASEI CPAN
0.06 tarball, SHA-256
`319601feec17fae344988a5ee91cfc6a0bcfe742af77dba254724c3268b2a60f`,
matching the publisher's `CHECKSUMS` entry. The official openEuler
24.03-LTS-SP3 riscv64 RVA23 primary has no same RPM/module provider and
supplies Time::Piece and Time::Seconds 1.3401 plus build/test tools.

The distribution README and sole installed PM both credit Dave Rolsky and
Marty Pauley and directly grant this program the same terms as Perl. No
contrary notice appears in the three tests, build file, Changes or metadata.
The package therefore declares GPL-1.0-or-later OR Artistic-1.0-Perl.

All three original default tests are unchanged and passed locally: 26
assertions without skips. Target `%check` requires the same suite and an
installed smoke test exercises date, datetime and timestamp conversions.
This PR does not merge or publish the package.
