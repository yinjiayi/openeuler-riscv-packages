# libbf

The official author homepage announces a new version on 2025-06-03 and links
the exact dated source archive. Its VERSION agrees. RPM Version is normalized
to 2025.06.03; the retained Arch-extra discovery row was 2021.03.27-1, not a
claim that the historical catalog already knew this release. The N225 capture
records SHA256 `4b23394d67a4a3c3266a38b66831094523fffb5d01974a5c05a0327b36b0a340`
for 150365 bytes, 26 members and 25 original files. No Git identity or publisher
checksum is invented. No offered signature was observed in the captured page,
author readme or archive; that does not assert global absence of every unseen
publisher endpoint. Automatic updates are disabled pending an explicit
upstream hyphenated-date to RPM dotted-date mapping, not guessed source URLs.

All 25 originals are copied before any added packaging material and installed
with their SHA256 manifest. Eighteen C/header/Makefile files contain complete
MIT grants; the author distributes the associated readme, VERSION and five
Pi-output checksum files with the same project. Original Charlie Gordon
copyright in readline.c and algorithm/idea references to GMP, MPFR and named
papers remain verbatim. The package adds Apache-2.0 SPEC/shell/QA material and
ships its complete unmodified legal text; it does not relabel upstream MIT.

Plain upstream `all` builds bfbench, bfpi and bfcalc. CONFIG_BFTEST, CONFIG_AVX2,
profiling, M32 and ASAN are originally off and remain off. Both portable NTT
multiplication and decimal arithmetic remain enabled. The original Makefile
does not build or install a library archive/shared object/pkg-config file and
has no install target. This package installs the original three executables,
adds libbf.a from the same libbf.o+cutils.o objects and installs libbf.h. It
does not claim a fabricated shared-library or upstream pkg-config interface.
Normal distro compiler/link flags are retained without forcing SIMD or LTO.

The full original `make test` is preserved: generate Pi at 100000 and 1000000
decimal digits and check both against the bundled SHA1 regression outputs.
Those SHA1 values are output oracles, not source authentication. `time` output
does not constitute a performance requirement or native benchmark claim.
The README statement that MPFR is used by default is stale relative to the
actual Makefile: MPFR, GMP and MPDecimal are only used by CONFIG_BFTEST=y.

Nondefault scope is explicit. bftest offers 39 operation labels, uses x86 rdtsc
without an architecture guard and repeats time-bounded random profiles forever
unless -S requests one pass; those operation labels are not a fixed observed
case count. It is not enabled or silently patched here. bfbench is built but
not run by make test; optional MPFR benchmark invokes gnuplot and can pause
interactively. Performance validation would require appropriate native evidence,
not blanket classification of the whole portable library as native-only.
bfcalc has 272 direct builtin bc_test calls behind -t, not invoked by original
make test and not counted as passes by this package. Interactive TTY behavior
does not establish privileged terminal/login/security validation.

Six added strict C cases cover context/integer addition/deep-copy independence,
parsing and owned formatting, two exact tie-rounding modes, division-by-zero
and invalid-root status, exact decimal addition, and 200-bit integer/subtraction/
square-root remainder. Installed smoke compiles that consumer again from only
installed headers/archive; a missing-library negative control must fail on all
six required symbols with no executable. GNU link trace and map must identify
the same actual installed libbf.a, and each required symbol must be defined in
the RISC-V ELF64 consumer. Exact seven-line output and empty stderr are required.
This is functional/static binding evidence, not a dynamic LD_DEBUG claim.
The installed manifest is generated in %check after RPM install-post stripping.

No original or added target code was compiled/executed during local onboarding.
Source-only verification and repository tooling tests are not target tests;
actual build/install/physical/publication evidence must come from subsequent
exact-head CI and independent product acceptance. Fresh canonical/open identity,
full official/fixed supplemental provider+namespace review and root-reviewed
atomic creation/repository gates remain required before submission.
