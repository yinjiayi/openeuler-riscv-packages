<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-makefun

This packaging README is Apache-2.0; unchanged external originals retain their
own BSD3 license and the attributed PEP380 public-domain source status.
The adapted tests/test_so.py::test_so_decorator excerpt is CC-BY-SA-4.0,
not BSD-only; full installed CC text and MAKEFUN-ATTRIBUTION.txt identify
Bite code/formerly e-satis, contributors/revision history, source title/URI
and upstream makefun.wraps/hello/assertion changes. Related Paolo Bergantino
example is conservatively attributed too. Pre2011 CC BY-SA2.5 section4(b)
allows the same-elements later4.0 license for this derivative. ShareAlike
is scoped to the adapted test excerpt, not the BSD3 library. No endorsement
or blanket BSD-only claim for Stack Overflow examples is made.

Official stable Git tag1.16.0 is fixed to commit197b14827c1b7830c0288477c007e1f1592f52ad;
all41 original Git/archive bytes retained. This is official stable Git authority,
not a current PyPI-latest or archive-GPG assertion. Frozen distribution lineage
keeps its original observation date and is not an upstream-source substitute.

Full BSD3 LICENSE and Sylvain Marie/Schneider Electric2019-2022 notices retained.
The legacy generator helper explicitly adapts PEP380 public-domain formal
semantics, with original attribution and removal/change note unchanged:
https://peps.python.org/pep-0380/#copyright . This is not a unique-copy-date claim.

Selected original GHA/nox CPython3.11 tests session uses coverage=False and
`python -m pytest --cache-clear -v tests/`. Original setup.cfg doctest discovery,
ignore_glob, warnings and all tests/skips remain unchanged. Target dependencies
are distro pytest7.4.4 and pytest-asyncio0.21.1. Its strict default may skip the
four original unmarked async test functions; those skips must be reported as
skips, not behavioral passes. A separate target-only asyncio.run replay awaits
the same four unchanged, hash-bound, no-fixture bodies and reports their actual
assertions independently. No marks/mode/filters/new skips are added.

Other interpreter/nox sessions, Python3.9 coverage70/report/badges, lint/docs,
build/release uploads remain preserved but unclaimed. No coverage value or
timing/performance/native-only result is inferred from the selected route.
SCM pretend version1.16.0 is bound to the fixed official Git tag for an archive
without .git. The original template-generated _version.py is AST-checked for
only the documented version/tuple assignments; its actual buildroot/installed
hash is recorded, not fabricated or treated as an original Git file.

Buildroot wheel and installed smoke run the same original suite plus the
separate replay. Scratch retains all tests/config but excludes source runtime.
All originals/archive/manifest/runtime/metadata are hash-bound and RPM-owned
on installed route; fail-closed fresh subprocess guards prove actual site
origins. No upstream/default/backend/RPM/QEMU executes locally. A submitted
hosted PR is not target CI, install, merge or publication acceptance.
