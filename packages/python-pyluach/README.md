<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-pyluach

This directory packages Pyluach 2.3.0 for openEuler 24.03 LTS SP3
`riscv64`/RVA23. The source RPM is `python-pyluach`, the installable RPM is
`python3-pyluach`, and the Python distribution and import namespace are `pyluach`.
External source licenses remain upstream's; Apache-2.0 covers only original
packaging metadata, scripts and documentation.

## Official source and license

The upstream `v2.3.0` tag resolves to fixed commit
`c1ffe4265f25ab7f5d850f4720111470f27e7ce5`. Its complete official Git archive
SHA-256 is `f8755477ae94b570e9717638570fab48dc00ed0c6d9255460b267aa9a87f888c`.
All 29 regular files match that immutable Git tree. The 12 non-generated
files in the official PyPI 2.3.0 sdist match the Git source; its generated
`PKG-INFO` is not substituted for the full source or original tests.
The sdist SHA-256 is
`ec6e30669d1df50c9ca160486da44a8195bb4c7a5d3d533990d0c5b03accd281`.

Retain the complete MIT `license.txt`, including copyright 2014 Meir S. List,
permission and disclaimer, in both source and binary redistributions.
The documentation retains its original 2016 MS List notice. No source,
license text, upstream recipes or patches are changed or imported. No separate
source signature was supplied by the observed official release metadata;
SHA-256 and the full fixed Git-tree identity are checked, not claimed as a signature.

The frozen `discovery-20260808T165000Z-9a89920c269462cd` record for
`github.com-simlist-pyluach` contains AUR `stale` and Debian `license-blocked`
decisions for historical 2.2.0 inputs. Those decisions are retained as history.
Fresh upstream 2.3.0 source contains an explicit complete MIT grant and matches
the publisher's sdist, which supplies the new admission evidence. Historical
distro versions are lineage, not current-source validation. AUR is never executed.

## Target dependencies and tests

Complete primary and filelists scans cover 18,503 official RVA23 and 1,192
supplemental RPMs, bound by SHA-256/size to fresh before/after unchanged
repository metadata and supplemental state. Neither repository supplies a
`pyluach` provider or owns its namespace; no managed directory or open canonical
package PR was present at the admission census.

Original `pyproject.toml` requires Python >=3.8 and `flit_core >=3.2,<4`.
The target supplies Python 3.11.6 and flit-core 3.8.0; pip 23.3.1 and wheel
0.40.0 build the unchanged backend without fetching dependencies. Original
test extras are pytest, pytest-cov, flake8 and BeautifulSoup: target RPMs
provide 7.4.4, 4.1.0, 7.0.0 and 4.12.2 respectively. They are declared, not vendored.
These are repository-provider facts, not proof of a completed DNF transaction.

`%check` retains upstream's `pytest --cov=src/pyluach tests/` and original
pytest configuration. The complete four test modules contain 143 static test
functions (not a measured runtime pass count); no filters, skips or tests are
removed. `PYTHONPATH=src` uses the unchanged source package corresponding to
upstream's editable install. The stale requirements export still names pyluach
2.1.0; upstream CI installs the unpinned pytest/cov/BeautifulSoup dependencies
and the current source instead, so that obsolete whole-environment export is
not used to replace or downgrade this release.

The installed smoke test checks the RPM, installed distribution/import versions
and fixed official date/holiday/calendar/reading examples. It is additional
installation coverage, not a substitute for the complete upstream `%check`.
The separate optional documentation build and Coveralls upload are not claimed
as reproduced by package tests. No native hardware or performance claim is made.

## Validation boundary

Trusted repository metadata tests, mock-based unit tests, golden source
materialization and official fixed-source verification are performed locally.
No upstream Python, build backend, RPM or QEMU is executed on the local host.
Target build, all upstream tests, RPM installation and smoke acceptance remain
pending CI on the exact PR head. The RISC-V state remains `unknown`; merge and
publication require independent current-head evidence and policy approval.
