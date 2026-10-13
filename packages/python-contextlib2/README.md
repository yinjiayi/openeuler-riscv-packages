# python-contextlib2

Current official Contextlib2 21.6.0, fixed Git tag21.6.0/commit
94174bafebe58a79af6059883f604624ab087d18. Discovery lineage is the exact frozen
Ubuntu contextlib2 21.6.0-1build1 row in snapshot
discovery-20260808T165000Z-9a89920c269462cd, not a fresh Ubuntu observation.
The official PyPI description and full source README link the Jazzband repo;
the frozen docs component is an identity lineage, not source checksum evidence.

All30 original Git files are SHA-256/Git-blob verified and retained, including
both whole test modules, original minimal test/support, all coverage/allowlist
settings, type hints, development patches and packaging configuration.
Original LICENSE.txt provides the full PSF2 notice for implementation/tests;
the included type hints are Apache2 as their original notice specifies.
Their exact fixed typeshed license is separate Source1 with its full Apache2
and conditional MIT text unchanged. These texts are installed as %license.
Packaging change summary: this adds an offline RPM wheel recipe and origin
verification wrapper and two declared compatibility patches. The runtime
implementation, support, configuration and all original30 retained files stay
unchanged. Only test_typo_enter/test_typo_exit in a separate compat copy
select AttributeError below Python3.11 or TypeError with the exact upstream
CPython3.11 message patterns on Python3.11+. Original author/legal notices and
the complete pristine source archive remain intact.

Python3.11 changed missing-context-protocol with-statement errors (bpo-12022),
as documented at https://docs.python.org/3.11/whatsnew/3.11.html#other-language-changes
and the same tests in https://github.com/python/cpython/blob/v3.11.6/Lib/test/test_contextlib.py
(Python3.10 still expects AttributeError). This patch preserves the original
negative-test intent, all discovered tests and the old-version assertion;
it does not accept an exception tuple, catch-all, skip, xfail or waiver.
The declared patch targets the fixed 21.6.0 source; its branch selects the
documented Python3.11+ semantics and retains the pre-3.11 assertion, without
claiming the legacy/PyPy matrix passed. It is a downstream test compatibility
patch, not an upstream-merged change. Remove it when a selected official
release carries the same version-compatible assertions, then re-audit the
whole source and full target defaults. The original PSF2 notice remains in
both copies; this change summary satisfies its derivative notice requirement.

The second patch changes only the shipped type-hint derivative of the fixed
21.6.0 stub. It declares five already implemented concrete context-manager
exit methods, and represents AsyncExitStack.__aenter__/__aexit__ as the actual
coroutine methods rather than synchronous methods returning an Awaitable.
The original mypy.stubtest failed under target mypy1.10.0 on these seven
declarations after all125 original tests and coverage96% had succeeded.
It is not a runtime change, mypy downgrade, allowlist extension or check waiver.
The original Apache2 attribution and fixed legal text remain unchanged; this
paragraph records the downstream derivative adjustment, not an upstream merge.
Remove the patch when a selected official source supplies equivalent concrete
exit/coroutine declarations, then re-audit the whole source and target defaults.
Static source/AST/patch inspection does not claim new stubtest or build success.

The complete selected original CPython tox defaults run on target Python3.11:
coverage run -m unittest discover -t . -s test; coverage report; coverage xml;
python -m mypy.stubtest --allowlist dev/mypy.allowlist contextlib2.
The two original deprecated-API allowlist entries remain unchanged; no new
skip, xfail, test expression filter, allowlist entry or coverage rule is added.
All original tests and inherited mixed-in test methods remain in discovery.
Legacy3.6–3.10/PyPy matrix, tox/Actions orchestration and external Codecov/PyPI
uploads are retained but not claimed validated. No pin or default is relaxed.

Source %check tests the staged wheel, not its source runtime. Installed smoke
repeats all four exact original commands against RPM-owned runtime with
all3 runtime hashes, distribution/version and fail-closed import-origin checks.
The implementation and py.typed retain their original hashes; the shipped stub
uses the declared derivative SHA, independently checked against an RPM-owned
compat copy, while its pristine original hash remains in original-files.json.
Both exact declared patch files and the compat stub are SHA/RPM-owner checked.
A fresh temporary test cwd includes pristine originals except for its absent
source contextlib2 copy and the one SHA-verified/RPM-owned compatible test copy,
preventing source shadowing without removing tests or masking runtime errors.
All30 originals and the immutable source archive remain intact in the RPM.
No local upstream/default/backend/RPM/QEMU execution is performed; local
checks are trusted repository validators/tests/golden and source-only verify.
Submission does not imply target CI success, merge or publication.
Inherited PYTHONHOME/PYTHONSTARTUP, coverage process startup and pytest injection
settings are removed; PYTHONPATH is replaced by the selected staged/installed
site. A guarded runtime preflight reports actual origin/hash, then unloads only
the verified candidate namespace before original coverage discovery. The guard
remains installed and exits fail-closed on origin/hash violation, even when an
original test catches import errors. No interpreter mode or default is changed.
