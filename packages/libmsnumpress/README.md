# libmsnumpress

This package is the independently documented C++ library component of MS Numpress,
not its separately documented Java, Python or C# implementations. The canonical
source is official tag `MsNumpress-0.2.3`, commit
`2657c2fe48ff9b5e11e87e31a7f5a16aef67bb0d`; all 14 regular archive files were
verified against official Git blobs. SHA-256:
`ef90d4ea214f6690b0430a148c053fbfb1595c669798f91dfa67fb3e5d24c4f5`.
Discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd` retains the AUR
1.0.0 lineage; that catalog number is not treated as an official release.

Original C++ source/header/test files carry Apache-2.0 grants and notices, which
remain unchanged. The complete official Apache license is an additional pinned
source. The README also permits BSD, but this package chooses Apache and does
not depend on the absent named BSD license file. No patch or borrowed recipe.

Upstream supplies no C++ build-system file. The recipe preserves the README's
direct `g++ MSNumpress.cpp MSNumpressTest.cpp -o test && ./test` approach, adding
target distro flags and `-UNDEBUG` so assertions remain effective. All 20 calls
in the original default main program must complete. Overflow checks retain the
upstream defaults. Additional functions not called by that original main remain
unchanged; this is not a claim of exhaustive or security testing.

Shared/static libraries, `.so.0` SONAME and pkg-config metadata are downstream
packaging choices, not a claim of upstream ABI stability. The unchanged default
suite is also compiled and replayed against both staged libraries and both
installed libraries. These four replays are not four new upstream suites. The
installed header and test source are checked against original SHA-256, shared
linkage/SONAME is checked, and RPM verification is mandatory. Unshipped language
bindings stay in the original SRPM source archive; their tests are not claimed.

Admission checked complete official/supplemental primary plus filelists, package
and capability naming, installation paths and dependency metadata closure. It is
not a substitute for real target DNF/build/install. Hosted CI must build offline
in the pinned openEuler 24.03 LTS SP3 riscv64/RVA23 image, execute original tests,
install RPMs and replay smoke checks. Physical RPM/SRPM verification and exact
head/current-main gates remain required before explicit squash. No local target
execution, Auto-merge, native, performance, security or publication claim.
