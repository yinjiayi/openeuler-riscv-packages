# Hash::FieldHash 0.15

Official source: `https://cpan.metacpan.org/authors/id/G/GF/GFUJI/Hash-FieldHash-0.15.tar.gz`.
The publisher `CHECKSUMS` in that directory gives SHA-256
`5c515707a5433796a5697b118ddbf1f216d13c5cd52f2b64292e76f7d9b7e8f1`.
The archive has one safe root, only regular files, and no patches.

The official `LICENSE` expressly grants GPL 1 or later or Artistic terms,
represented as `GPL-1.0-or-later OR Artistic-1.0-Perl`. The license is
installed in the RPM. `Build.PL` imports the archive's bundled
`builder/MyBuilder.pm`; the SPEC's `-I.` makes this verified source path
available explicitly without altering source code or assertions.

With an isolated official Test::LeakTrace 0.17 test dependency, the
unmodified local default `./Build test` passes all 21 files and 237
assertions, including leak and thread cases, without skips. Upstream
`t/05_threads.t` emits six nonfatal numeric preincrement warnings. Only
hosted target CI can establish openEuler SP3 RVA23/Perl 5.38 compilation,
test, RPM installation and smoke behavior.

The frozen 151,852-row inventory contains stale AUR `0.15-3` lineage;
it is not the authority for source, licensing, or dependencies.
