<!-- SPDX-License-Identifier: MIT -->
# sselp

Packages the [official stable 0.2 release](https://tools.suckless.org/x/sselp/)
for openEuler 24.03 LTS SP3, riscv64/RVA23. Sselp prints the X11 PRIMARY
selection as UTF-8, adding one newline after a nonempty selection. It is not
a clipboard manager or INCR/full ICCCM conformance implementation.

The fixed official source is https://dl.suckless.org/tools/sselp-0.2.tar.gz,
SHA-256 `cd0f95ec0eb571a6dd3c48ba3aa931080eb33bc81805bd72832cc04c01b8b822`.
All five original files were reviewed. The original MIT license credits
Anselm R Garbe (2006-2008); its exact bytes are retained in both binary packages,
with the original README and source archive. No published detached signature
was supplied by the official release index; SHA-256 is enforced. AUR `sselp`
0.2-1 in discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`
is lineage only, not a trusted recipe or evidence of a newer release.

The original default `all`/`install` targets, C99, `-pedantic`, `-Wall`, `-Os`,
VERSION define and libc/Xlib linkage remain. RPM flags are added; upstream
linker `-s` is omitted so normal RPM processing owns stripping/debug products.
There is no original test/check target to remove or skip. Build dependencies
come from the configured official target repository; the build/check phase
is networkless and unprivileged. Tests require Python3, libX11 and Xvfb.

Patch `0001-correct-property-chunk-offset-and-validation.patch` is a locally
authored MIT, downstream-only generic correctness fix, not a RISC-V workaround.
Original format-8 lengths count bytes but XGetWindowProperty offsets count
32-bit units: the original offset skips data after the first 16 KiB chunk.
The patch uses rounded-up 32-bit units, resets failed/refused reads, rejects
non-UTF8_STRING or non-8-bit properties, checks allocation and releases Xlib
storage. It does not change successful small-selection bytes, empty/no-display
success or the original newline convention. No upstream write was made.
Remove it when a stable release fixes these cases and passes these regressions.

`%check` runs the same owned Python suite against the staged tree that the
installed smoke invokes from `sselp-tests`. Fifteen named check groups retain
the original source/license/README and exact version/no-display behavior, then
use a fresh private Xvfb display and an owned PRIMARY selection provider for
no owner, empty/ASCII/UTF-8/embedded-NUL/existing-newline selections, 16383,
16384, 16385 and 32769 byte boundaries, conversion refusal and malformed
32-bit property format. Exact stdout, stderr, status and request counts are
asserted with finite deadlines and process/display cleanup. This tests protocol
fixtures, not native desktop input, timing, performance, security or exhaustive
ICCCM behavior. Allocation exhaustion is statically guarded, not fault-injected.

Local checks are repository metadata/test/golden and source/patch verification
only, with no upstream source execution or RPM/QEMU build. Hosted CI must still
prove the exact head's target build, staged checks, ordinary installation and
installed smoke. Physical RPM/SRPM and fresh main/required CI acceptance are
mandatory before any explicit squash; Auto-merge stays off. Publication is a
separate immutable metadata and physical-product gate, never inferred here.
