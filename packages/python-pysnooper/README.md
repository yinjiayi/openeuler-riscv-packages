# python-pysnooper

Current official PySnooper 1.2.3, fixed tag1.2.3/commit
0561a89c0ec88d11f38c6ef815d12c0423300fe1. Fedora python-pysnooper1.2.3-7.fc44
and openSUSE python-PySnooper1.2.3-1.4 are exact frozen Aug8 discovery lineage,
not current distribution observations. The stale separate AUR row is not used.
All43 original Git files and the complete fixed source archive are retained.

The complete source licensing is MIT AND PSF-2.0, not a claim that all vendored
support is MIT. Original PySnooper MIT copyright2019 Ram Rachum/collaborators
is preserved. tests/mini_toolbox/pathlib.py retains copyright2014–2017 Matthias
C. M. Troffaes and2012–2014 Antoine Pitrou/contributors with its MIT header.
The full original pathlib source is installed visibly as %license alongside
the full MIT permission text. Vendored tests/mini_toolbox/contextlib.py is
byte/AST-identical to official contextlib2.py at v0.5.4 commit
d533028739d643830af03bf23255b5d4f8535108, not a guessed copy version/date.
That samecommit full PSF2 LICENSE.txt is fixed Source1 and installed as %license,
retaining its history/copyright2001–2011/terms without substitutions.
Packaging change summary: offline wheel/RPM recipe, intact original test/support
and origin-verification wrapper; no upstream implementation, support, test,
timing tolerance, configuration or assertion is changed.

The selected shared original tox command is pytest {posargs} with no posargs
on target CPython3.11. Original tox.ini strict-markers and every original test
remain in unfiltered discovery. Functional clock/trace checks preserve original
0.2 tolerance and sleeps/assertions; they are not performance benchmarks.
Legacy2.7/3.4–3.10/PyPy, flake8/pylint/bandit/readme/requirements/clean jobs,
tox/Travis orchestration and release publishing are retained but unclaimed.
No test filter, new skip/xfail, pin relaxation or clock waiver is added.

Source %check tests staged wheel runtime; installed smoke repeats original
pytest against actual RPM-owned runtime with all5 source hashes and exact
distribution/version checked. All43 originals/immutablearchive/license are
also RPM-owned. A fresh test cwd copies byte-identical original config/tests/
support but not the source runtime package; fail-closed import guards keep
all runtime imports bound to staged/installed bytes even if tests catch errors.
Inherited interpreter/pytest injection and PYSNOOPER_DISABLED are removed,
PYTHONPATH replaced by selected site, no interpreter mode/default change.
No local upstream/default/backend/RPM/QEMU execution. Submission is not target
CI success, merge or publication; actual target CI determines compatibility.
