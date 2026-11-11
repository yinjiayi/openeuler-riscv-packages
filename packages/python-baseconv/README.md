# python-baseconv 1.2.2

Official stable tag 1.2.2 is fixed to semente/python-baseconv commit
505b5fd7b11855182e760704fec5461974033644 (repository: semente/python-baseconv).
All seven complete original Git files and their full PSF version 2 license and
Guilherme Gondim, Simon Willison and Drew Perttula notices are retained. AUR
python-baseconv 1.2.2-4 metadata and active Fedora Everything-source
python-baseconv 1.2.2-8.fc44 inventory lineage are discovery evidence, never
executable packaging. Stale AUR lineage alone is not an admission basis.
Fedora observation is the immutable 2026-08-08T16:50:00Z inventory, not a claim
of a fresh Fedora fetch. Its evidence link is the exact committed discovery
snapshot, whose retained Fedora metadata names the official release-index URL
https://download.fedoraproject.org/pub/fedora/linux/releases/ and the observed
Everything-source primary SHA-256
c2dcdc609d12c90294d8bbe3589901a14826c1f6f088c9f88853bc87a8883f9a.

The selected original shared core Travis test argv is exactly
`coverage run baseconv.py`. All 20 module doctest examples and all 1,414 original
round-trip assertions remain. Target Python 3.11 uses supplied coverage, not an
online pip install. The historical Python 2.7/3.4/3.5/3.6 matrix and separate
external Coveralls installation/reporting remain unvalidated and uninstalled;
they are not counted as tests passed. No original core test assertion is removed.

The declared local patch removes only an obsolete Python 2 L integer suffix in
the module and README example, preserving its exact value and expected answer.
It retains the doctest result, counts completed original loop assertions, logs
actual attempted/failed doctests and assertions, and propagates any doctest
failure after the complete unchanged loop. This is the PSF clause 3 brief summary
of derivative changes. It is not a RISC-V instruction fix or test relaxation.
Patch provenance is the complete fixed official source above; it is not submitted
upstream because upstream writes are unauthorized. Remove only after a verified
new upstream release fixes both compatibility and failure propagation and retains
the same complete default contract. The ordered patch is explicitly SPEC-applied.

Build requires target Python devel/pip/setuptools/wheel and coverage. Upstream
runtime has no third-party dependency; coverage is retained for installed smoke.
The wheel is built offline, no dependency download or isolated build backend,
with SOURCE_DATE_EPOCH=315532800. Original setup.py publish/upload is never used.

Installed-origin validation means every tested baseconv import and executed
script resolves to the exact patched module owned by this RPM, not a pristine
source-copy shadow. The immutable original archive, all pristine source files,
their SHA-256 manifest and the declared patch are installed under
/usr/share/python-baseconv. A fresh scratch symlink named baseconv.py points to
the hash-verified installed module, preserving original test argv and discovery.
A fail-closed startup guard binds doctest imports to this same installed origin.
Exact actual output must show 20 attempted/0 failed doctests and 1,414 completed
assertions. The same complete route runs against the buildroot wheel in %check
and the installed RPM in smoke, with ownership checked only for installed RPM.

No local upstream/default/backend/RPM/QEMU execution is used for onboarding.
Trusted repository and source-only validation do not establish target success;
only exact-head CI and physical products can prove build/install results.
Pure Python; RISC-V state remains unknown pending target CI.
