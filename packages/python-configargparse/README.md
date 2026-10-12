<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-configargparse

ConfigArgParse1.8.0 is a pure Python argument parser for openEuler24.03-LTSSP3,
Python3.11 and riscv64/RVA23. Source is immutable official `v1.8.0` release
commit `eba8686d82c007569f93b82c43a686ad7f68f6b3`, not a moving Git branch.
SHA-256 `910e8bd128e94a1ba3befad1549a5cece5285b7bc89fae6c0b713783088aaa55`
binds the archive; all17 regular Git blobs match its official Git tree.
Original MIT LICENSE, source, tests, configuration and workflows are retained
unchanged in the owned archive. No upstream patch is added.

Frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`,
canonical `github.com-bw2-configargparse`, has Arch/Fedora/openSUSE1.7.5 lineage.
Those records discover the component; current official PyPI1.8.0 and formal Git
tag verify this newer stable release. No distribution recipe is executed.
The initial PyPI sdist LibreSSL transport failure is not verified sdist bytes;
the independent full fixed official Git release is used instead.

The selected default is the original CI test job's Python3.11 route:
`pytest --cov-branch --cov-context=test --cov=.`. All seven unversioned test
extras are supplied: black, mock, toml, PyYAML, pytest, pytest-cov and
pytest-subtests. Check runs the whole original suite, including its original
expected failures. Upstream imports `test.test_argparse` and otherwise logs that
many compatibility tests could not run; this recipe requires that full module
from actual python3-devel3.11.6 rather than accepting the omission. Independent
Python3.13 Zizmor/Pydoctor lint, other interpreters/platform matrix, aggregate
coverage and publish jobs stay unchanged but are not this target environment
or claimed successful. No target3.11 test is waived or altered.

Supplied setuptools, setuptools-scm7.1.0 and wheel build offline.
`SETUPTOOLS_SCM_PRETEND_VERSION=1.8.0` is the standard fixed-release input for
this archive without .git; setup.py is not rewritten or imported locally.

Installed smoke verifies RPM ownership, exact version/runtime/archive hashes,
extracts all17 original blobs, isolates only the temporary source runtime
outside collection and reruns the same complete original argv against the
physical installed module under an import guard. Every test/configuration
stays byte-identical. No installed coverage percentage is claimed merely from
`--cov=.` in the scratch test directory.

Admission joins complete official18503 and supplemental1211 primary/filelists,
finds no canonical/managed/capability/module/file-owner/reverse conflict, and
records a163-package/1439-edge static closure with40 non-EQ constraints retained
for review. This is metadata feasibility, not a DNF solver or target success.
Dependency names are actual target RPM names, not guessed aliases.

No upstream/default/backend/target/RPM/QEMU runs locally. Trusted repository
validation and source-only verification precede the PR. Exact-head CI must
still build/install/run all original tests and verify real RPM/SRPM before
merging. QEMU is not native RISC-V, ABI or production evidence. No Auto-merge.
