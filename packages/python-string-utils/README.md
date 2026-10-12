<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-string-utils

Packages the complete official String Utils 1.0.0 release for openEuler 24.03
LTS SP3 riscv64/RVA23, fixed at Git commit
`d903db3c24de35c5cb7e1229ebbcc19775a952a8` and full archive SHA-256
`60b76619a1015853ea9a3f9d106c159ac82aa110c54c635a7e2ba6d376fb797c`.
The six runtime files match the formal PyPI sdist byte-for-byte. The formal
Git archive supplies the omitted full LICENSE, original build/default configs
and all 42 original test files. All 69 original Git blobs remain in the RPM's
fixed original archive; there are no source patches.

Upstream's full LICENSE and setup.py identify MIT. Frozen AUR metadata says
Apache and stale, but it is discovery lineage, not legal or current-release
authority. Live official PyPI still reports stable 1.0.0. The repository's
Apache-2.0 license applies only to original packaging, not upstream source.

The default test is the unchanged `python -m unittest` from tox.ini. There are
407 statically identified methods, not 407 locally passed tests. CI must run
the entire original suite at source build and against RPM-owned installed
runtime, with all original tests and no new filters/skips. Python 3.11 is the
target; the historical py35-py38 tox matrix is not claimed as tested.

The original `build.sh` and its `python setup.py sdist bdist_wheel` are retained
and replayed offline using the supplied setuptools/wheel and a private Python
3.11 executable binding. Historical dev.requirements.txt covers development,
docs and release tooling and is retained, not installed as tox test deps.
The unchanged upstream installation writes README data to `/usr/README/README.md`;
packaging relocates identical bytes into `/usr/share/doc/python-string-utils/README.md`
to avoid a generic shared data path. This is packaging layout, not a source
or default-test waiver.

Installed smoke verifies the full archive, six runtime files, README and all
43 test-package Python files (including empty __init__.py) against original
bytes and RPM ownership, executes the whole default from a scratch tree with
no source runtime shadow, then independently replays the original build.
No local upstream/default/backend/RPM/QEMU execution or target CI success is
claimed during PR preparation. Native hardware/performance claims are absent.
