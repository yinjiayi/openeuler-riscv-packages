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
verification wrapper; it changes no upstream module, type hint, test, support,
configuration or assertion. Original author/legal notices remain intact.

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
A fresh temporary test cwd includes byte-identical originals except for its
source contextlib2 copy, preventing source shadowing without removing tests.
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
