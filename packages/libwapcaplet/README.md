# libwapcaplet 0.4.3

Official fixed NetSurf release, SHA-256
`9b2aa1dd6d6645f8e992b3697fdbd87f0c0e1da5721fa54ed29b484d13160c5c`.
All 12 original files, MIT COPYING and frozen Arch extra 0.4.3-4 lineage
are retained; distribution metadata is not executable source evidence.

Keep upstream default static release build and original `make test`, then
run the same original suite for a shared release build and an additional
static `VARIANT=debug` build. Upstream release sets NDEBUG, selecting 21
tests; debug additionally selects 11 original assertion/signal tests.
The original runner already comments out its unimplemented memory suite;
the recipe makes no source/test changes and does not remove default tests.

Both staged and installed checks compile unchanged upstream testmain.c and
basictests.c against shared and static installed release libraries. They
use the matching upstream release NDEBUG policy, compare the header and
verify shared linkage. Complete original source is shipped for offline QA.
NetSurf buildsystem >=1.10 and Check >=0.9.5 are actual repository dependencies.
No local source/RPM/QEMU build was run. Exact target CI and physical artifacts
remain required; this is not native hardware or performance validation.
