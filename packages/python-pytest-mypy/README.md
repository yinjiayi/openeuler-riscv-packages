<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-pytest-mypy

Packages official pytest-mypy 1.0.1 (MIT) for openEuler 24.03 LTS SP3,
RISC-V RVA23. Fixed PyPI sdist SHA-256:
`3f5fcaff75c80dccc6b68cf5ecc28e1bbe71e95309469eb7a28bf408ce55c074`.
All 13 original Git files at formal-release commit
`1b3e931cb6ff00b47436455c69e3cd978b745479` match the sdist byte for byte;
the eight additional sdist files are generated packaging metadata.

No source patch or configuration rewrite. The setuptools >=61/scm >=7.1
backend and filelock >=3/mypy >=1/pytest >=7 runtime requirements are retained.
The complete original pytest command keeps branch coverage >=100%, xdist,
pytester subprocesses, looponfail and all original skip/xfail markers.
Source `%check` imports the built wheel; installed smoke tests copy only the
original tests/config into a fresh directory without a runtime shadow.

Target Python 3.11 corresponds to the upstream Python-3.11 test matrix, using
target pytest 7.4.4, mypy 1.10, xdist 3.3.1, cov 4.1 and randomly 3.15.
Packaging 24.2 differs from the upstream tox test-environment pin ~=21.3;
this is a disclosed target-tool compatibility boundary, not an observed failure
or permission to remove tests. The original tox file remains unchanged.
Other Python-version environments, Python-3.12 static analysis and Twine upload
are separate upstream development/publication contexts, not native-target claims.
No local upstream, backend, default-test, RPM or QEMU execution was performed.
CI run 38167854174 (head 03b77733ba3c3868c00ca7a28acbea88bb236bf7)
collected 84 target items with four xdist workers, showed a failure, then hit the
existing build deadline (inner exit 124). The retained log lacks failing node IDs
and a traceback; installation did not run. No source root cause is claimed.
Both source and installed whole defaults now append only outer CLI `-vv -rA`
for running/failing node diagnostics; no options are exported to nested pytester.
Original tests, skip/xfail, xdist, 100% branch-coverage gate and deadlines remain
unchanged. This is not a repair-success claim; the new head needs full fresh CI.

External source retains the MIT license. Apache-2.0 covers original packaging only.
