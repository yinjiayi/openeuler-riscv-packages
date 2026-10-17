<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-frozendict

This directory packages upstream `https://github.com/Marco-Sulla/python-frozendict` version `2.4.7` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery canonical row `python-frozendict` and its official GitHub
component map to upstream import/distribution `frozendict`, source RPM
`python-frozendict`, and binary RPM `python3-frozendict`. Historical Arch,
Debian, Fedora and openSUSE lineages are preserved; they are not current build
or license evidence.

Source0 is the immutable official stable v2.4.7 Git commit
`d4ee7590e2b507fd68124cd8a593778ce3c1158b`, SHA-256
`ef1fdbca09c6e3e8d2969d059e2a231f62e89958363a752a2d0ca2930c714ee1`.
All 82 Git blobs were compared with the inert archive. Official PyPI also
identifies 2.4.7 as the latest version; its sdist has 65 identical source
members, generated packaging metadata and five differing older C-source
members. This recipe consistently uses the Git release source, without mixing
sdist members. SHA-256 establishes byte identity, not an author signature.

The actual source includes the complete LGPL version 3 license. Preserve it
with its complete GPL version 3 companion and a conservatively restored full
official CPython 3.10.2 notice for copied dict implementation. The exact
original copied CPython revision is unknown: the supplemental notice version
does not assert source ancestry. All original source and notices remain
unchanged; all three complete notices are installed by `%license` and retained
in the SRPM. Conflicting historical distribution MIT labels do not override
the actual upstream source license.

Keep the original optional-C setuptools backend without setting
`FROZENDICT_PURE_PY` or `CIBUILDWHEEL`. Upstream supplies C-source directories
only through Python 3.10, and its C-wheel workflow excludes CPython 3.11 and
later. The target Python 3.11 backend behavior and documented pure-Python
fallback remain pending real CI, not claimed as successful locally. Preserve
the backend's architecture-specific wheel policy; do not assert a noarch
payload before target build evidence.

The initial exact-head CI run `38086896843` on `18fe80b0156502de423e8d4bac21b60ba3504ac7`
observed the original optional-C fallback and completed all 262 runtime pytest
items, 100% branch coverage and the original mypy checker. RPM packaging then
failed because its automatic debuginfo subpackage had an empty `debugfiles.list`;
no RPM/SRPM or installed-smoke success followed. This recipe suppresses only
that inapplicable debug subpackage for the pinned target's Python-only payload,
not the optional C attempt, backend or tests. Re-evaluate this packaging choice
when a future source/target actually builds an ELF extension. A repaired head
still requires its own complete target build/install and physical artifacts.

The entire upstream target-3.11 sdist default suite is retained: pytest with
100% branch coverage, followed by the original `test/run_type_checker.py`
mypy command. No tests, flags or gates are removed or patched. The upstream
CPython 3.11 C-wheel exclusion is not counted as a successful C-only debug
test. Coverage uses a fresh output name, and pytest/mypy resolve the staged
wheel payload. The installed smoke separately checks RPM ownership, version,
typing files, immutable operations, deep freezing, hash and pickle behavior;
it is not a substitute for the full default suite.

Fresh checksum-bound target repository scans cover all 18,503 official and
1,192 supplemental records. Required suppliers include Python/devel 3.11.6,
setuptools 68.0.0, wheel 0.40.0, pip 23.3.1, pytest 7.4.4, pytest-cov 4.1.0,
coverage 7.3.2, mypy 1.10.0 and typing-extensions 4.12.2. Original checker and
backend declare no higher version floor; compatibility remains for CI to
prove. The preliminary missing-mypy claim was incorrect and was corrected
against complete official Provides metadata. No canonical provider,
top-level module/distribution namespace or reverse-constraint conflicts were
found; Jedi's nested typeshed stub is not a top-level module owner.

Local checks are limited to trusted repository validation and source-only
materialization. No local upstream code, backend, default suite, RPM or QEMU
was executed. Real target build/default-test/install results and physical
RPM/SRPM evidence remain mandatory before merge or publication.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
