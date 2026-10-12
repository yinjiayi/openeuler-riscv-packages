# Algorithm::Combinatorics 0.27

Official source: `https://cpan.metacpan.org/authors/id/F/FX/FXN/Algorithm-Combinatorics-0.27.tar.gz`.
The publisher `CHECKSUMS` in that CPAN directory records SHA-256
`8378da39ecdb37d5cc89cc130a3b1353fd75d56c7690905673473fe4c25cd132`.
The archive has one safe root and only regular files/directories.

The official source README and module POD explicitly grant the same terms as
Perl itself. This is represented as `GPL-1.0-or-later OR Artistic-1.0-Perl`;
legacy `META.yml` says `unknown` and is not a contrary license grant. The
README is installed as the RPM license notice.

The unmodified default `make test` runs 17 files and 361 assertions on local
Perl 5.34.1. Its optional `t/pod-coverage.t` skips locally because
`Test::Pod::Coverage` is absent. The SPEC requires the official target
provider so the complete default test suite can run on openEuler SP3 RVA23.
The target also supplies the XS compiler and Perl development headers;
target compile, test, RPM install, and smoke results are CI evidence, not
inferred from the local macOS run.

The frozen 151,852-row inventory records a stale AUR `0.27-2` lineage;
it is not the authority for source, licensing, or dependency decisions.
