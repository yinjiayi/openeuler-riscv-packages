<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-addict

This directory packages official `mewwts/addict` latest stable `2.4.0` for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The canonical component is
`github.com-mewwts-addict`; the source RPM is `python-addict`, and binary RPM
`python3-addict` provides that name. Original pure-Python dictionary attribute,
item, child-class, copy, pickle, union and freeze features remain enabled.

## Fixed official source and license

Source0 pins the official `2.4.0` release tag at commit
`338936265dd924ec5892aeee9c122d7e4f77680d`, archive SHA-256
`de2f0b25ec39068a04954092b9ef98660229ee1293fc24d6b8230cbb566f6f4a`.
All ten original Git blobs are retained. Fresh official PyPI metadata agrees
that `2.4.0` is the latest stable release; the independent checksum-verified
PyPI sdist has byte-identical shared original files. No sdist file overrides
Source0, no older-version workaround and no source patches.

The complete original MIT `LICENSE` credits 2014 Mats Julian Olsen; unchanged
installed module metadata also retains its 2014–2020 copyright. The original
license is shipped with `%license`. Frozen stale AUR and non-stale openSUSE
lineage remains discovery evidence, not executable recipes or release/license
authority. Official tag, source files and latest PyPI resolve the original
unverified-upstream decision without rewriting raw frozen decisions. GitHub's
API reports signed-commit verification (`verified=true`, `reason=valid`). This
is an API report, not local PGP or archive signature verification; the archive
remains independently SHA-256-bound.

## Complete original acceptance

The original GitHub workflow runs `pytest` without exclusions or version pins.
Tracked Travis additionally runs `coverage run --source=addict setup.py test`,
and the README documents `python -m unittest -v test_addict`. All three full
source-side commands are preserved using target Python 3:

```text
python3 -m pytest
python3 -m coverage run --source=addict setup.py test
python3 -m unittest -v test_addict
```

All 64 static test methods remain unchanged, including inherited methods in
both `DictTests` and `ChildDictTests`; 64 is not an observed runtime count or
pass result. No alternative discovery, selected-case filter, disabled default
feature or ignored exit code is used. The optional bare standalone script
runs two runners without explicitly propagating unsuccessful results, so it is
not used instead of the original workflow and documented CLI failure gates.
Target Python 3.11 compatibility remains pending CI, not inferred from other
upstream Python/OS matrix jobs or static review.

The original setuptools build is kept, including its dynamic module version
read and `test_suite` metadata. Supplied setuptools 68 retains that deprecated
test command and raises a failure if its original unittest suite is not
successful; this was checked in its checksum-bound official source, not run
locally. Source `%check` isolates `COVERAGE_FILE` at a fresh generated path
without changing the original `--source=addict` or test loader. Coverage 7.3.2,
Python 3.11.6, setuptools 68.0.0 and pytest 7.4.4 are available in complete
checksum-bound repository metadata.
`python3-pytest` is a build dependency and an explicit installed acceptance
dependency; upstream library code itself has no third-party runtime imports.
No network build dependency installation or backend replacement occurs.
Travis `coveralls` after_success is an external coverage publication step,
excluded under the no-upstream-write boundary, not a test failure ignored or a
source test removed. No additional coverage threshold/report gate is invented.

Installed smoke runs outside the source tree in fresh scratch with inherited
`PYTHONPATH` removed. It verifies RPM ownership of the imported installed
module, its implementation and the unmodified installed original test. Only
the test is copied byte-identically into scratch; no library shadow copy is
created. Both original pytest and documented unittest CLI suites then import
installed RPM-owned code. Original coverage `setup.py test` is source-build
acceptance in `%check`, not falsely described as installed-code coverage.

Complete fresh official and supplemental primary/filelists metadata, current
main package/upstream metadata and all open PR actual paths were screened.
No same canonical package, matching module/provider, owned namespace or
reverse requirement was found. Final live-main/head/canonical/source/supplier
checks remain mandatory before submission. Trusted repository validation and
source-only evidence do not establish target build, installation, native
validation or publication; those require matching actual CI and products.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
