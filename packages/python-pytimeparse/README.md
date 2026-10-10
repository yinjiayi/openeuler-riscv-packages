<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-pytimeparse

Packages official `pytimeparse 1.1.9` for openEuler 24.03 LTS SP3,
`riscv64`/RVA23. Runtime RPM `python3-pytimeparse` is pure Python/noarch,
requiring Python >= 3.11. This is not the separate pytimeparse2 fork.

## Source and discovery

Official PyPI metadata `https://pypi.org/pypi/pytimeparse/json` identifies
upstream `https://github.com/wroberts/pytimeparse`. Release tag `1.1.9`
resolves to fixed commit `c62ae66cbfc4a71b745a265842f179266391d953`.
The complete official GitHub archive has SHA-256
`7cb94d4a1931cf609827ef23d2abcff03268d7b1615bc9e3f65de958e37cb919`.
All 12 regular source files, including both tests, were checked against official
Git blob identities. Tag/commit is unsigned; no verified signature is claimed.
Keep exact MIT `LICENSE.rst` and inline notices; original packaging is Apache-2.0,
not a relicensing of upstream source.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` associates canonical
`github.com-wroberts-pytimeparse` with Arch, Debian, openSUSE and Ubuntu lineage
at older 1.1.8/1.1.5 releases. Its historical `unverified-upstream` decision is
retained, not rewritten into source evidence. New official release verification
admits this particular 1.1.9.

## Dependencies and complete tests

Only the configured official RVA23 repository is needed: Python 3.11.6,
setuptools 68.0.0, wheel 0.40.0, pip 23.3.1 and pynose 1.4.8 were found in
checksum/size-bound primary metadata. A complete filelists scan found no
existing pytimeparse module owner. These are admission observations, not target
installation/build success or a supplemental-provider guarantee.

Build unchanged setup.py with `sdist bdist_wheel`, then install the wheel with
`--no-index --no-deps`. Upstream declares `nose.collector` as `test_suite`;
official `python3-pynose` supplies that same nose module/collector with Python
3.11 fixes. `%check` invokes that entry point directly, rather than allowing
deprecated setup.py test to fetch the obsolete `nose` distribution requirement.
No source patch, filter, expected-failure or skip is introduced. Collection must
run all 57 original unittest methods across both modules, including the original
doctest method, succeed and report zero skipped tests. Travis coverage<4/coveralls
is a reporting/upload wrapper, not another core-test suite; no coverage claim.

Installed smoke checks RPM ownership, exact metadata/source version and parsing
regressions, then both complete installed TestCase modules (57 methods, no skips)
using stdlib unittest and isolated Python imports. Nose remains build-only.
Wheel timestamps clamp only pre-1980 SOURCE_DATE_EPOCH, preserving later epochs.
No network is required by build/test logic; actual CI network policy must still
be reported as observed.

## Acceptance boundary

Time expression parsing is arithmetic, not hardware/wall-clock performance.
No RISC-V patch or native-only reason is identified. Status stays unknown until
exact-head CI proves build, full check, RPM installation and installed smoke.
Local checks exercise trusted repository tooling/source verification only;
no upstream backend/test or local RPM/QEMU execution. No automatic merge,
product URL, publication or trusted-runner recovery is claimed.
