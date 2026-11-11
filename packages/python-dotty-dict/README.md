# python-dotty-dict 1.3.1

Official stable tag v1.3.1 is bound to immutable pawelzny/dotty_dict commit
74c527265e56a46a2485561fbc74646a063df5da, tree
6777c84bc263e53338a084ae0c5a78779669a0a9. The complete archive contains37
original Git files; full MIT copyright/license and every original test/config
remain unchanged. Frozen Arch/Debian/Ubuntu lineage is discovery evidence,
not executable packaging.

The original shared core entry point is bare pytest. Its unchanged pyproject
sets testpaths=['tests'] and addopts='-rx -s --verbose'. All 79 total test nodes,
including test_examples (which invokes every original example function),
remain unfiltered. The report-only external observer records actual collection,
pass/fail/skip/xfail results and fails acceptance unless all79 pass with zero
skips/xfails; it does not modify selection or outcomes.

The target is CPython3.11, outside the original legacy CI interpreter matrix.
Original CPython Poetry dev pytest7.1.2 pins and poetry.lock remain untouched
but are not claimed reproduced. Upstream PyPy CI independently runs bare
pytest with an unconstrained pytest install. This package preserves the full
core suite on the target; it does not claim the entire Poetrylock/tox/lint/docs
or historical interpreter matrix. No requirement or source was patched.

PEP517 uses original poetry_core>=1.0.0. BuildRequires are target Python
devel/pip/poetry-core>=1.0.0/pytest; runtime is Python only. pytest is retained
for the full installed smoke route. SOURCE_DATE_EPOCH=315532800 and offline
pip wheel/install avoid dependency downloads or isolated build environments.

Installed-origin validation means both dotty_dict Python files match immutable
original hashes, and every import resolves to those buildroot/installed RPM
files. A fail-closed startup import guard binds exact absolute paths before
pytest. Fresh scratch tests contain all pristine originals except the source
runtime package, preventing source-copy shadowing; original configs/tests,
examples and pyproject hashes are rechecked before and after. All37 originals
and the pinned archive are retained under /usr/share/python-dotty-dict.
The same full route runs in %check against the buildroot wheel, then smoke
against installed RPM ownership. This is not a source/default execution claim
before exact-head target CI and physical artifacts are verified.

No local upstream/default/backend/RPM/QEMU execution was used for onboarding.
Trusted repository tests and offline source verification are not target build
or installation proof. RISC-V status remains unknown pending CI.
