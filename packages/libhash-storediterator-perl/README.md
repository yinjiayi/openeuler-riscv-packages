# Hash::StoredIterator 0.008

Official source: `https://cpan.metacpan.org/authors/id/M/MS/MSCHWERN/Hash-StoredIterator-0.008.tar.gz`.
The publisher `CHECKSUMS` in that directory gives SHA-256
`b9cbc4dcd8233e8d1d7f1481ddb79a4a5f9db7180cb3ef02b4bcbee05e65ea0c`.
The archive has one safe root, only regular files/directories, and no patches.

The source `LICENSE` expressly grants the same terms as Perl itself and
includes the GPL 1 or later and Artistic license texts. The RPM therefore
declares `GPL-1.0-or-later OR Artistic-1.0-Perl` and installs that license.

The unmodified local XS build and default `./Build test` pass the one
upstream test file with six top-level Test2 tests and no skips on Perl 5.34.1.
The source accesses Perl hash-iterator state through the Perl C API without
architecture-specific assembly. Only hosted target CI can establish its
Perl 5.38, openEuler SP3 RVA23 compilation, complete test and installed-smoke
behavior; this local check is not target-build evidence.

The frozen 151,852-row inventory contains stale AUR `0.008-3` lineage; it is
not the authority for source, licensing, dependencies, or test results.
