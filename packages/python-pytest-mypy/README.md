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

The replacement head `276cb00107408469d9c52468eda04a917a9354f8` also
timed out in run 38178063989: all 84 items were collected, with 21 passes and
one original xfail before the unchanged deadline. No failed node or traceback
was reported. Four last-running worker nodes are inferred from completion
order, not proven hung operations; the earlier find-debuginfo warning did not
stop execution before `%check` and is not the timeout cause.
Both outer commands now add only `-o faulthandler_timeout=300`: pytest's
non-exiting, per-item Python stack dump after 300 seconds, not a test deadline.
The official target pytest7.4.4/xdist3.3.1/execnet2.0.2 sources support propagation
to outer workers and their original stderr. Original nested pytester arguments
and output assertions remain unchanged; no environment options or hooks are
injected. Target stack retention is an expected path awaiting new-head CI,
not an observed result. Outer stacks may show a subprocess wait without proving
its child's internal cause. No source repair, native-only classification,
test selection change, worker-count change or deadline extension is claimed.

Run 38186267156, exact head `1c8e763b2130437c7363237e90a88b673fe42f2f`,
collected all 84 items and completed 23 passes, two original xfails and a failure
in `test_mypy_encoding_warnings` before the existing build deadline. Outer
faulthandler stacks show pytester subprocess waits; some such waits later passed,
so a stack alone is not a deadlock or native-only diagnosis. The failed warning
test's assertion traceback was not retained before the deadline.

Both outer launchers now call public `pytest.main` with exactly the same argv
and an explicit controller-only report object. On each failed report it writes
the full traceback and captured sections as an ASCII-safe JSON record to a
flushed duplicate of the original stderr descriptor. The descriptor is marked
non-inheritable; the object is not exported to xdist workers or nested pytester
children. Original source, child arguments, all 84 items/29 test functions,
skip/xfail markers, xdist, 100% branch coverage and deadlines remain unchanged.
This is a concrete diagnostic input, not a source fix or CI-success claim.
Four fake-report tests verify only this reporting code's forwarding and output
contract; they are not target pytest execution. Full replacement-head CI is
still required, and child-process root cause remains unresolved.

External source retains the MIT license. Apache-2.0 covers original packaging only.

Current failed head `756074d34fee5d40f29c5f05cf5bfade8cf454db`, run
38199709664, completed 15 passes and one original xfail of 84 collected
items before an observed 3127.015-second build-phase timeout. It produced no
failed TestReport. Some 300-second parent subprocess waits subsequently passed;
this does not establish a source defect, deadlock or native-only requirement.
The earlier controller-only reporter cannot inspect an unfinished pytester
child. Target pytest 7.4.4's original pytester writes each child's stdout/stderr
to fixed files and only dumps them after that child exits.

Both outer launchers now additionally start a packaging-only read-only daemon
in the controller. Every 60 seconds it records only that controller's descendant
PIDs, parent PIDs, process state, CPU ticks and process-start identity (maximum
64 descendants, with explicit truncation). For descendant working directories
inside `/tmp` with a `pytest-` path component, it reads only pytester's fixed
`stdout`/`stderr` regular files, at most the last 2048 bytes of each. Directory
and file opens reject symlinks; nonblocking opens reject FIFOs without waiting.
ASCII JSON records distinguish missing/racing observations and PID reuse. A
shared lock serializes complete observer/controller report writes; a concurrent
fixture exercises both producers against a deliberately split-write sink. It
never reads environment variables or command arguments, signals a process,
modifies a child file, or injects a plugin, environment option or argument into
workers/pytester children. This daemon is stopped after the original pytest
call; the original pytest return code is returned unchanged. It neither
terminates tests nor extends the build deadline.

All original source bytes, 84 collected items/29 test functions, skip/xfail
markers, worker selection, 100% branch coverage, nested subprocess arguments,
source and installed defaults and existing deadlines remain unchanged. The
20 fake-proc/temp fixtures exercise only this new observer's parsing, scope,
size limits, symlink/FIFO rejection, PID identity and lifecycle. They are not
upstream or target-test passes. This is a diagnostic-content change, not a
causal timeout fix or target-CI success claim; new-head full CI remains required.
