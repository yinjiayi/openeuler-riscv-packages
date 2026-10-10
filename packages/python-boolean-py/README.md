<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-boolean-py

Packages official boolean.py 5.0 for openEuler 24.03 LTS SP3, riscv64/RVA23. The canonical/source RPM name is `python-boolean-py`; the binary RPM is `python3-boolean-py`, the Python distribution is `boolean.py`, and the import namespace is `boolean`. These names are deliberately distinguished; this is supplemental supply, not replacement of a known official owner.

## Immutable source and lineage

Official stable tag `5.0` resolves to `8a443837e68dc027004294fb17fe1857cf783410`. Its fixed-commit GitHub archive has SHA-256 `5a2ee926209a30d2790b3fe81e06d207ab666901e6e662269aa10bacd5c2ce4c`. All 23 regular archive files match the complete Git tree by path, byte size and Git blob SHA. The separately advertised official PyPI 5.0 sdist was checksum verified: 22 shared files match byte-for-byte; its shared `setup.cfg` has identical configuration values, with only setuptools formatting and generated empty `[egg_info]` fields. Seven sdist-only files are generated distribution metadata. Packaging retains the original Git files, without changing the upstream version, backend or configuration.

Frozen discovery `discovery-20260808T165000Z-9a89920c269462cd`, component `github.com-bastikr-boolean.py`, has four actual distribution observations: Arch extra `python-boolean.py` 5.0-2, Debian stable/main 4.0-4, Fedora Everything-source 5.0-10.fc44 and openSUSE oss 5.0-1.4. These are catalog lineage, not an invented AUR observation and not proof that those external recipes were executed.

The full BSD-2-Clause notice in `LICENSE.txt` is installed as `%license`; upstream `README.rst` and `CHANGELOG.rst` are retained. The original `.github/workflows/test-and-build.yml` separately retains its complete MIT grant and Brotli Authors attribution in the Source/SRPM materialization. That workflow-file license is not a project-wide MIT license and is not substituted for the runtime module's BSD-2-Clause license; no upstream workflow code is copied into the packaging scripts.

## Target dependency and namespace admission

Admission rehashed all 18,503 official and 1,192 supplemental primary/filelists entries against unchanged fresh repomd and supplemental state before and after scanning. No existing boolean.py package/capability provider, reverse distribution constraint, or owner of the Python `boolean` namespace was found. The supplemental HTTP metadata binding is a read-only input check, not a build-machine trust recovery or public-release assertion.

Official providers are Python/devel 3.11.6-20.oe2403sp3, pip 23.3.1-7.oe2403sp3, setuptools 68.0.0-2.oe2403sp3, wheel 1:0.40.0-1.oe2403sp3, pytest 7.4.4-1.oe2403sp3 and pytest-xdist 3.3.1-1.oe2403sp3. The original setuptools backend has no version floor, no runtime dependencies, and its testing extra requires `pytest >= 6, != 7.0.0` and `pytest-xdist >= 2`; these supplied versions satisfy those bounds. The original version-5.0 changelog drops Python before 3.9, compatible with target Python 3.11.6; the older README's Python 3.6+ wording is not used to lower that boundary.

Target wheel 0.40.0's original `safe_name`/`safer_name` and `wheel_dist_name`/dist-info construction preserve the distribution's dot. The SPEC therefore installs `boolean.py-5.0-py3-none-any.whl` and owns `boolean.py-5.0.dist-info`, not the modern published wheel's `boolean_py` spelling. This was confirmed by checksum-verified official wheel 0.40.0 source inspection, without running that backend.

## Original package gate and evidence boundary

`%check` runs the original tox and test-workflow command, `python3 -m pytest -vvs boolean`, including the complete original `setup.cfg`: all Python files, doctest modules, strict markers, original recursion exclusions and expected-failure annotations. The three original package Python modules contain 86 static test definitions; this is not a runtime passed-test count. An explicit version guard preserves the testing extra's pytest 7.0.0 exclusion. The original source test files and default selection are not filtered, patched or disabled.

This is the complete original test suite for the single SP3 Python environment, not upstream's multi-OS/multi-Python matrix. Separate upstream wheel/sdist release checks, documentation jobs and PyPI publication are not claimed as reproduced; optional lint/docs/development extras are not runtime requirements. The installed smoke separately checks the installed distribution version/location and documented parse/simplify plus absorption and De Morgan APIs; that limited API smoke does not replace full `%check`.

Build and installation are offline (`--no-index`, `--no-build-isolation`, `--no-deps`), using the declared target providers. Local validation runs only trusted repository validation/test/golden checks and source-only verification; it does not execute upstream code, the backend, RPM or QEMU. Actual target build, default-test and installed-smoke success requires exact-head CI and physical artifacts. Submission does not authorize merge, trust restoration or publication.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
