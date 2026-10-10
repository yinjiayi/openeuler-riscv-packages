<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-crccheck

Packages Martin Scharrer's stable crccheck 1.3.1 for openEuler 24.03 LTS SP3
`riscv64`/RVA23. The pure-Python payload is `python3-crccheck` (`noarch` does not
mean target validation has succeeded).

## Identity, source and notices

The retained frozen component is `github.com-martinscharrer-crccheck`, with AUR,
Debian, openSUSE and Ubuntu discovery lineage. It is unrelated to the GitHub
account `crccheck`'s Django project. Distribution rows are discovery evidence,
not recipes or executable input; none were executed.

Source0 is the original unyanked official PyPI 1.3.1 sdist, SHA-256
`1544c0110bf0a697d875d4f29dc40d7079f9d4d402a9317383f55f90ca72563a`.
All 33 original Git files in its 39 regular members match immutable official
`v1.3.1` commit `94f1b0967fdb59428e2702391fe3390a41c6ead1`. Six additional
members are release-generated metadata, including PKG-INFO with Version 1.3.1;
they are not claimed as Git blobs. This preserves setuptools-scm's original
release metadata without forcing a version environment variable.
No detached signature was supplied with that official PyPI release. HTTPS,
published SHA-256 and complete fixed-tag source comparison are used; no
signature verification is claimed. Full MIT LICENSE.txt and per-file notices
remain intact, and LICENSE.txt is installed by `%license`. No patches.

## Backend and default tests

Keep `setuptools.build_meta`, `setuptools>=61.2` and `setuptools_scm[toml]>=7`.
Build the original sdist and wheel offline with `python3 -m build --no-isolation`;
pip installs that wheel with no index/dependencies. No legacy backend or C/native
override.

The upstream Makefile's default `all: test` runs all three commands:

```
python -m coverage run --branch -m unittest discover
python -m coverage report
python -m coverage html
```

`%check` retains this complete default sequence using the target `python3`.
The four test modules contain 79 statically counted test definitions, which is
not an observed runtime count. Original random inputs, subtests and .coveragerc
remain unchanged; there is no upstream fail-under threshold to invent. A fresh
COVERAGE_FILE prevents stale data. Upstream's separate `doc` and external PyPI
release/publish targets are not substituted for, or counted as, default tests.

Installed smoke verifies the installed module's path and actual RPM ownership,
release metadata, two known CRC vectors and the module CLI. It then copies only
the unchanged tests and .coveragerc into a fresh directory and repeats all three
default commands against the installed module. Coverage is consequently a
declared test-support runtime requirement, not an upstream library dependency.

## Admission and validation boundary

Complete official 18503 and supplemental 1192 primary/filelists entries were
checked with freshly rebound immutable metadata. No crccheck module,
distribution capability, reverse dependency or overlapping Python payload was
found. The mysql-test `rpl_crc_check` file-name substring is an unrelated SQL
replication test, not this module. Target suppliers include Python 3.11.6,
setuptools 68.0.0, setuptools-scm 7.1.0, build 1.0.3, coverage 7.3.2, pip 23.3.1,
wheel 0.40.0 and tomli 2.0.1. Main and all open PR actual files were separately
checked for the canonical component; a fresh fence is required before submission.

Only trusted repository validation and source verification may run locally.
No upstream module, backend, default test, RPM or QEMU has run locally. Actual
target build, default-suite result, physical RPM/SRPM and install smoke remain
pending CI; this recipe makes no build-success or publication claim.
