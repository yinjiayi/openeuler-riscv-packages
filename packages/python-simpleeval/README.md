<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-simpleeval

Simpleeval 1.0.8 targets openEuler 24.03 LTS SP3, riscv64/RVA23. The full official
Git archive is fixed to commit `e4466b7a69f8e7420dbce003d99f5e8c0562367c`, SHA-256
`8f1849cb8668b828b480c8be2723eff90003a9872136479b2a77a6ce3f984c0e`.
The official stable PyPI metadata independently identifies release 1.0.8; its
sdist has SHA-256 `b417f869c11f2de034eb919820a825f35d12ce99f63a43971947ce73679eb9ba`.
All released runtime, tests, metadata and MIT notices match the full Git source;
the latter additionally retains the omitted original Makefile and CI defaults.

The selected original target-interpreter route is the complete
`python -Werror -m unittest` Makefile/tox base command and the independent GitHub
Python 3.11 test job's `coverage run -m unittest` and `coverage xml`. On the
official target, coverage 7.3.2 exposes `coverage.cmdline:main` through
`python3 -m coverage` rather than an unversioned executable; only that entrypoint
spelling is mapped, with all original arguments and collection preserved.
No test selection, skip, fixture or upstream source is changed. All 160 static
test-method definitions and original interpreter-dependent decorators are
retained; this is a source inventory, not an executed or passing test count.

The separate original Python 3.14 uv/ruff/mypy lint/build job, developer groups,
external Codecov reporting and complete CPython/PyPy/Windows interpreter matrix
are preserved in the archive but are not claimed successful on target Python
3.11. The Python 3.11 original test job does not install those separate developer
tools. The normal offline wheel packaging uses supplied Hatchling 1.27.0; its
availability and dependency bounds are metadata feasibility, not a local build.
The wheel command scopes `SOURCE_DATE_EPOCH=315532800` to the ZIP format's 1980
timestamp lower bound; this fixed reproducible build input replaces CI's epoch0
only for wheel creation and does not modify any source, default test or fixture.

`%check` uses a pristine full release to isolate generated wheel/build copies.
The installed smoke verifies every retained original file, checks RPM ownership
and bytes of installed `simpleeval.py`, copies the complete unchanged tests into
an isolated scratch directory without the source runtime, and guards every
runtime import before repeating the entire original target test route.
Tests and backend/RPM execution belong to repository CI, not local onboarding.
No RPM/SRPM URL or target-success claim is made before verified CI artifacts.

Frozen AUR/Debian/Fedora/openSUSE/Ubuntu rows are discovery provenance only;
historical versions are not claims about current upstream or target supply.
Upstream MIT notices remain unchanged. Repository Apache-2.0 covers packaging
only. Simpleeval is not a production security boundary.
