# libclaw 1.9.1

Fixed official tag `1.9.1` points to unsigned commit
`c3762283e2fffe795cc1462289f0da40834acb8a`. The original upstream CMake
project and generated header report **1.9.0**; the recipe preserves that value
and identifies the distribution by the tag, without inventing an ABI update.

The official fixed archive SHA-256 is
`6f136ad09e3db3ef59d7b6af43f3d539f93b6590ea155815b82333cfb9644529`.
All 429 archive files matched Git bytes and executable modes. The two omitted
export-ignore Git metadata files are separately fixed Sources, making the
retained source set all 431 Git files. No implementation/test/license file
was omitted by the archive. Tag, commit and matching official release have
no available signatures; this is unsigned official source, not verified GPG.

Defaults are retained: seven static archives plus the header-only core,
French localization, full Doxygen HTML, and all 21 installed example source
archives. No shared libraries are enabled in place of the default static
build. The multilib patch changes only the CMake configuration destination
to relative `lib64/cmake/claw`; exports and staged consumers remain relocatable.
Static archive debug compiler flags remain intact; only an empty standalone
ELF-debuginfo package is suppressed.

The original `test/check-examples.sh` is unchanged and compiles all 21
installed example archives. It does not register CTest or run application
runtime assertions and does not itself return failure for its failure count.
The wrapper therefore requires exactly 21 archive files, 21 `[PASS]` lines,
one `21 pass, 0 fail.` summary and no `[FAIL]`. It runs during `%check` from
the staged installed tree and again after normal installation. A separate
downstream installed CMake consumer links all seven modules and checks image
dimensions and a finite known linear easing value with assertions enabled.
It is not an upstream algorithm/performance suite. Old standalone runtime
fixtures remain in the original archives but are not substituted for the
upstream default compile-only suite. No local upstream/RPM/QEMU execution was
used to prepare this recipe; target execution and physical RPM acceptance
remain mandatory hosted-CI gates before merge.

Library/template/example notices are retained as LGPL-2.1-or-later, including
both Julien Jorge and Sebastien Angibaud notices where present. Original
COPYING is the full LGPL2.1 text. The full GPL2 reference companion is carried
without relicensing the library. `example/tween/mkpng.gp` is an unchanged
GNUplot save-generated configuration with the original Thomas Williams/
Colin Kelley banner. A fixed SPDX full gnuplot permission companion is included
conservatively for that banner; the composite RPM License field does not
claim the library implementation or every binary uses the gnuplot license.
New packaging-only QA is LGPL-2.1-or-later and its source is retained in SRPM.
