# Algorithm::Permute

Algorithm::Permute 0.17 provides XS permutation iterators and callbacks.
The frozen inventory record `libalgorithm-permute-perl` has Debian and Ubuntu
lineage. The official author's CPAN CHECKSUMS matches the pinned archive
SHA-256; bundled LICENSE resolves its inventory license-review hold with the
Perl GPL/Artistic grant. Static archive review found 26 ordinary entries under
one root.

The official openEuler SP3 RVA23 primary metadata with SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`
contains neither the RPM name nor module provider. It supplies Test::LeakTrace
0.17, so this package does not rely on a pending supplier PR.

`%check` retains all four default test files and enables upstream
`AUTHOR_TESTING=1 MEMORY_TEST=1` gates to exercise POD and the five Linux leak
checks. The upstream tied-array TODO is retained as declared by upstream;
CI logs must report it accurately. Installed smoke verifies six distinct
permutations, reset and twelve ordered pairs. Locked target CI performs the
XS build and tests; no local RPM/QEMU build, native performance or public
publication claim follows from source verification.
