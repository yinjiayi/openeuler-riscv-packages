# List::Gen 0.979

Official source: `https://cpan.metacpan.org/authors/id/S/SO/SOMMREY/List-Gen-0.979.tar.gz`.
The publisher `CHECKSUMS` in the same directory records SHA-256
`dc4a4affa792162c3023cc7c79e17cc753720cd3d5bbcb63aaa93c3141396a1d`.
The archive has one safe root and only regular files/directories. The main
module grants GPL or Artistic terms, consistent with CPAN `perl_5` metadata.
The frozen AUR 0.974 row is stale lineage only; 0.979 is the official current
stable release.

The unmodified default local `make test` passed 18 files and 1,634 assertions.
Its POD coverage file skipped because optional Test::Pod::Coverage was missing
locally. The fixed target repository has Test::Pod::Coverage 1.10 and
Pod::Coverage 0.23, both declared as BuildRequires, along with Test::Pod 1.52
to exercise the full default suite on the target. The upstream manifest author
tests remain conditional on `RELEASE_TESTING`. No tests are edited or disabled.

The verified official SP3 RVA23 primary metadata has no `perl(List::Gen)` or
`perl(List::Generator)` provider or same-name RPM. It has the required Perl,
MakeMaker, Filter::Simple, Scalar::Util, List::Util, and test providers.
