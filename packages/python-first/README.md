# python-first 2.0.2

Official stable tag 2.0.2, immutable hynek/first commit
294964dd2b7a68930ff520a58cdb314e58ecb1e7. Full MIT copyright/license is retained.
The pinned archive contains all 14 original Git files; none is patched.
Actual AUR python-first 2.0.2-7 metadata supplies discovery lineage, not executable packaging.

The selected upstream shared test entry point is `make test`, unchanged from
Travis. Its original Makefile runs `python -m pytest --doctest-glob='*.rst'
--doctest-modules --ignore=setup.py`; all unit tests and module/RST doctests
remain present. A private interpreter shim binds original `python` to target
Python 3.11. Separate `make cov`, legacy Python matrix, tox manifest and
external PyPI-description routes remain intact but are not claimed executed.

BuildRequires are target Python devel/pip/setuptools/wheel/pytest and make;
runtime has no upstream third-party dependency. pytest and make are retained
for the complete installed smoke route. Wheels are built offline with fixed
SOURCE_DATE_EPOCH=315532800, no dependency download or isolated build backend.

Installed-origin validation means every tested `first` import resolves to the
hash-verified module owned by this RPM, not a source-copy shadow. All pristine
originals and the pinned source archive are retained under /usr/share/python-first.
Fresh scratch tests copy every original except first.py; first.py is a symlink
to the verified installed module, preserving default module-doctest discovery.
A fail-closed startup guard loads that exact module before pytest and validates
its real origin. The original Makefile and command arguments are unchanged.
The same full route runs against the buildroot wheel in %check, then against
the installed RPM in smoke. All source/config/test hashes are rechecked.

No local upstream/default/backend/RPM/QEMU execution was used for onboarding.
Source-only and trusted repository validation are not target build/install
proof; only exact-head CI and physical products can establish those results.
Pure Python/no native-kernel requirement; RISC-V status remains unknown pending CI.
