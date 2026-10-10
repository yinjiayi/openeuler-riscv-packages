# python-aenum

Upstream: <https://github.com/ethanfurman/aenum>, latest official stable 3.1.17.
Target: openEuler 24.03 LTS SP3, riscv64, RVA23. Target build and installed
acceptance remain pending CI; no upstream backend, tests or RPM ran locally.

## Official source and notice closure

Source0 is official tag `3.1.17`, fixed at commit
`f0f6fd8e2ac0bb379eb11f6029023d2bad88732a`, SHA-256
`b4fbd11dc2444b2b10d6ceb211441878e2fc0d39881a4fdda369514eea8b425d`.
All 19 regular Git blobs were checked. The same-version official PyPI sdist omits
`test_v37.py`, although the original default imports it, so it cannot alone
preserve that suite. Source1 is that immutable PyPI sdist, SHA-256
`a969a4516b194895de72c875ece355f17c0d272146f7fda346ef74f93cf4d5ba`;
only `aenum/README.md` (byte-identical to Git's root README) and original
`doc/aenum.pdf` are extracted. No library or test file is replaced.

Complete original BSD-3-Clause `aenum/LICENSE` is retained. Python-derived code
additionally carries the complete official CPython 3.11.6 LICENSE, fixed at
`8b6ee5ba3bd08368ba3c763cea28ce1464a88e62`, SHA-256
`3b2f81fe21d181c499c59a256c8e1968455d6689d269aa85373bfb6af41da3bf`.
This is conservative full-notice restoration, not a claim that 3.11.6 was the
exact copied revision. No upstream code is modified; downstream changes are the
RPM recipe, notice restoration and installed verification described here.
Original `CHANGES` and documentation are shipped with the notices.

## Original defaults and target suppliers

Build check and installed smoke retain `python3 -m aenum.test`: original main
temporary-directory handling, `test_v3`/`test_v37`, `load_tests`, module doctests
and `doc/aenum.rst` doctests. Original version-based skips remain unchanged.
Explicit target-supplied `python3-pyparsing` preserves optional parser cases;
no dependency-absence skip is introduced. Original standalone
`test_stdlib_tests.py` remains present but is not imported by this default.
Static test definitions are not an observed runtime pass count.

Original setuptools/distutils build/install are retained, including original
Python-3 installation removal of Python-2-only `_py2.py`. The target install macro
uses `--skip-build`: the recipe removes only its stale generated
`build/lib/aenum/_py2.py` before original install, so Python-2 syntax is not
installed or bytecompiled on Python 3. Original source bytes remain untouched
before the upstream install's own filtering. Build networking is disabled.
Functional threaded uniqueness cases retain their assertions, without
a timing/performance gate or asserted native validation. Installed smoke checks
the imported module is RPM-owned by `python3-aenum`, then runs the original suite
outside the source tree.

Complete official 18,503-entry and immutable supplemental 1,192-entry primary and
filelists scans found no existing aenum provider, module owner or reverse
constraint. Python 3.11.6, setuptools 68.0.0 and pyparsing 3.1.1 are target-supplied.
Frozen AUR, Debian, Fedora, openSUSE and Ubuntu lineage versions remain separate
from the newly verified official release. Managed metadata and all open PR actual
paths were screened; submission requires a fresh competing-head/main fence.
