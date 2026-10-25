# python-iterable-io 1.0.4

Official stable tag v1.0.4 is pinned to pR0Ps/iterable-io commit
9cdce76c27930cc1db80b360a9c22b7dc3b35828 and tree
f01e5085674e7f890f2de5c13ed580440aba1514. All seven original Git files,
including complete library, tests, README, build metadata and original CI,
remain unchanged and are retained with the immutable archive in the RPM.
Fresh official Arch Extra JSON observed 2026-10-13T20:51:38.191123+00:00 confirms
python-iterable-io 1.0.4-1 and upstream identity; this is an actual primary
observation, not an invented retained distribution snapshot.

Upstream declares LGPL-3.0-only but does not bundle a license text. This
package adds both verbatim LGPL-3.0-only.txt and GPL-3.0-only.txt as supplemental
terms from official SPDX license-list-data v3.29.0 commit
31ba1a50e5397e00a304dbadc76531740e89ee48. Each is separately SHA-256 pinned in
sources.yaml and shipped using %license; their FSF copyright and verbatim-copy
permission are preserved. They are not claimed original upstream files or
successful direct GNU downloads. The upstream LGPL-3.0-only declaration and
GNU URL are unchanged; this does not change the license to -or-later.
The packaging review is not broad legal advice.

Original PEP517 hatchling.build and its unchanged requires=['hatchling']
remain. Original CI builds with python -m build . --wheel, installs the wheel,
then runs the entire unfiltered py.test --cov=iterableio suite on Python3.11.
The remote recipe uses that wheel frontend with --no-isolation for the supplied
offline build environment; no dependency is downloaded by the backend.
Runtime is standard library only. pytest/pytest-cov/coverage are retained for
the complete installed smoke route; no new coverage threshold is added.

Installed-origin validation means all seven original hashes and the sole
iterableio runtime hash match the fixed Git source, and every candidate import
resolves to the selected buildroot/installed wheel. Candidate import origins
are checked by a fail-closed finder/audit guard. A separate preflight child
cannot preload library statements before pytest-cov starts. All pristine
tests/configs are relocated unchanged without source-library shadowing.
The same full coverage suite runs against the buildroot wheel in %check and
against RPM-owned paths in smoke. Isolated JUnit reporting only records
outcomes; strict expected20 tests/zero failures/errors/skips is a future
acceptance assertion, not a claim that the tests have already passed.
Separate OS/interpreter CI matrix routes are retained but unclaimed.

No source/backend/default/RPM/QEMU build was executed locally. Static
120-package/945-edge closure and 25 reviewed non-EQ supplier bounds are
admission evidence, not DNF solving, ABI/native verification or target build
success. Trusted repository392 tests and offline verify-only remain distinct
from exact-head CI, RPM/SRPM and installed-default acceptance.
