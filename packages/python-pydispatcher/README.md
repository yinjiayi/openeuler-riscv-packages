<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-pydispatcher

Packages PyDispatcher 2.0.7 for openEuler 24.03 LTS SP3 riscv64/RVA23.
BSD-3-Clause covers PyDispatcher; Python-2.0 applies to the Python-derived
documentation helper and reference documentation. Apache-2.0 covers original
packaging only. The full actual official CPython historical LICENSE from
commit f3ebc9fe3fae3d44da4d0da9764ed7c033115f12 is preserved as Python-LICENSE,
SHA-256 8129570d0752f342973e176c87123b7b7199b6f8a907a4b6704d4473b3dd2d3b.
Observed docmodule derivation shares 21 whole AST statements with Python's
HTMLDoc.docmodule; the upstream changes add whole-package context handling
and DefaultFormatter subclass overrides. This is a derivative-change summary,
not a claim to know the exact historical copying commit. Original helper,
generated weakref reference docs, notices and all source files stay unmodified.

The official release tag's immutable Git commit ec403b24e163b926150f2cadaf8e7a8c057f0749
retains all 45 original blobs, full BSD notice, four whole test modules,
tox.ini, requirements and documentation. The released PyPI source shares all
original files except setup.cfg's normalization and generated empty egg_info
appendix; the unchanged Git configuration is used. The actual Arch extra
python-pydispatcher 2.0.7-4 row is discovery lineage, not target-build proof.

Both engines retain the original shared tox command: pytest --cov=pydispatch
--no-cov-on-fail --cov-report=term-missing tests. Whole original tests, including
installed-version packaging metadata, run on target Python 3.11 without added
filters, skips, source patches, coverage thresholds or removed features.
Original tox interpreter matrix ends at Python 3.10 and is retained/unclaimed;
this recipe does not claim upstream selected an original 3.11 matrix job.
The standalone legacy covertest.sh nose utility is retained but not selected
by the original tox default route. Runtime has no original extra requirement;
unmodified original pytest/pytest-cov requirements are supplied explicitly.

Each engine uses a fresh complete non-runtime source copy without a local
pydispatch directory. Original SHA-256 import guard checks installed modules
without preloading before coverage; installed smoke verifies every RPM-owned
original file, runtime module, archive and installed dist-info. Only explicitly
matched RPM-generated Python caches may be extra. Backend wheel construction
is offline using supplied setuptools/wheel and a fixed 1980 ZIP timestamp.

Trusted local repository checks and source-only verification are not target
build evidence. Original defaults, backend, RPM and installed execution occur
only in actual CI; CI success, RPM/SRPM links and publication remain unverified.
