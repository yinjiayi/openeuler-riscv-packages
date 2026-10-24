# Algorithm::Permute

Algorithm::Permute 0.17 provides XS permutation iterators and callbacks.
The frozen inventory record `libalgorithm-permute-perl` has Debian and Ubuntu
lineage. The official author's CPAN CHECKSUMS matches the pinned archive
SHA-256. Static archive review found 26 ordinary entries under one root.

This draft remains held for license review. The generic bundled LICENSE grants
Perl GPL/Artistic terms, but four source headers add a commercial CD-ROM or
similar-media restriction requiring prior author approval: `Permute.xs` lines
6–9, `coollex.c` and `coollex.h` lines 4–7, and `lib/Algorithm/Permute.pm` lines
5–8. No author clarification resolves this contradiction.
`LicenseRef-Algorithm-Permute-CDROM-Commercial-Restriction` is the local name for
that unresolved file-specific notice; it is not an approval of redistribution.
Source redistribution is marked false, maintenance is update-disabled, and
automatic updates are disabled. Do not merge or publish this package until
author evidence or an independently verified clarified release resolves the hold.
The pinned source bytes and their original notices remain unchanged.

The earlier exact-head CI run passed technically, including installed smoke
and product hashes; that result does not establish license clearance and does
not apply automatically to this corrected commit. The earlier claim that the
inventory license hold was resolved was incorrect.

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
