# Math::ConvexHull for openEuler RVA23

This package pins official CPAN Math-ConvexHull 1.04 at SHA-256
`b9041f08d58792308f204455a67a265799e88b279e5c2f54e3f8dee9594c0852`,
matching the publisher's `S/SM/SMUELLER/CHECKSUMS`. Frozen Ubuntu
`libmath-convexhull-perl` 1.4-2 gives package lineage: its original source
archive MD5 `5d9225c5fadf5c71172cd88c81661d4d` equals the official
CPAN 1.04 archive, despite Debian's normalized version spelling. Official
openEuler 24.03-LTS-SP3 riscv64 RVA23 primary metadata has neither
`perl-Math-ConvexHull` nor `perl(Math::ConvexHull)` and supplies its Perl,
List::Util, Data::Dumper and test dependencies.

The module POD and upstream README expressly grant redistribution under
Perl 5 terms; no included file has a conflicting notice. The RPM installs
upstream README as license evidence. `%check` runs all four original t files,
with target `Test::Pod` and `Test::Pod::Coverage` BuildRequires enabling both
POD tests. Local macOS source tests passed 34 assertions, but skipped POD
coverage because that optional module was absent; this is not target proof.
Installed smoke checks the RPM/provider, version and a four-corner hull.
Target test execution and installation require exact-head hosted CI; PR
artifacts do not establish public repository publication.
