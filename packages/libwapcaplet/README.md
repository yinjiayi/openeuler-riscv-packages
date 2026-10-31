# libwapcaplet 0.4.3

Official fixed NetSurf release, SHA-256
`9b2aa1dd6d6645f8e992b3697fdbd87f0c0e1da5721fa54ed29b484d13160c5c`.
All 12 original files, MIT COPYING and frozen Arch extra 0.4.3-4 lineage
are retained; distribution metadata is not executable source evidence.

Keep upstream default static release build and original `make test`, then
run the same original suite for a shared release build and an additional
static `VARIANT=debug` build. Upstream release sets NDEBUG, selecting 21
tests; debug additionally selects 11 original assertion/signal tests.
The first target build reached the additional debug compilation, where the
buildsystem's default -O0 conflicts with target _FORTIFY_SOURCE=2 and -Werror.
Only that additional build/test uses CCNOOPT=-O1; DEBUG, assertions, fortify,
warning errors, all original tests and default release settings remain enabled.
The original runner already comments out its unimplemented memory suite;
no suite registration or expected assertion/signal is removed.

Check0.15.2's deprecated fail_unless appends an extra NULL to its printf-
annotated failure function, making the original suite fail format-extra-args
under Werror. The local MIT compatibility patch follows existing
[upstream issue2887](https://bugs.netsurf-browser.org/mantis/view.php?id=2887)
and the [fixed Check0.15.2 API](https://raw.githubusercontent.com/libcheck/check/11970a7e112dfe243a2e68773f014687df2900e8/src/check.h.in).
It changes only62 assertion API names:53 with messages to ck_assert_msg and
9 without messages to ck_assert. All predicates/messages,32 registrations,
fixtures and expected signals are byte-preserved; no warning is suppressed.
This is a local not-submitted backport, not an accepted upstream fix; remove
it when a release ports the complete suite equivalently.

Both staged and installed checks compile unchanged upstream testmain.c and
the same compatibility-patched basictests.c with Wall/Werror/Wformat=2
against shared and static installed release libraries. They
use the matching upstream release NDEBUG policy, compare the header and
verify shared linkage. Complete original source plus the patched assertion
driver are shipped for offline QA.
NetSurf buildsystem >=1.10 and Check >=0.9.6 are repository dependencies.
No local source/RPM/QEMU build was run. Exact target CI and physical artifacts
remain required; this is not native hardware or performance validation.
