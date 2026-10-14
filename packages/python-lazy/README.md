# python-lazy 2.0

Build the untouched fixed official lazy-2.0.tar.gz sdist (Source0, SHA-256
f92ec0d32dd6bd115ddec4e3323473ebc0b682ad58c6aca78ebfd9e6d1aa5777).
Source1 retains all24 originals from official annotated tag2.0 →
df4694a225d89df54fe2ef871b84f3d96832e7ac →
83c65f9c09d2fe39e8a1e0692ae06878cb09eba1.
The stable sdist clears Git egg_info tag_build=dev0; original config is preserved
separately and never patched. Root inert proof39e5b53f identifies this release
difference; it is not local backend execution or target success.

Preserve full BSD-2-Clause LICENSE/copyright. All24 original files and both
fixed archives remain in RPM/SRPM; runtime four files are checked byte-for-byte.
No patch is applied. Packaging/guard helpers have separate Apache-2.0 scope.

Target-only default checks independently cover source, wheel, buildroot and
installed RPM: unchanged python -m unittest discover, all45 exact original
test IDs and zero additional skips; python -m mypy --strict --exclude lazy/tests
lazy; python lazy/examples/example.py. These are acceptance requirements, not
observed passes. Driver uses original argv through stdlib runpy and reports
that boundary, not a bare-launcher claim. Installed tests import actual
RPM-owned runtime files under a fail-closed origin/hash guard. Type checking
reads a scratch runtime copied from and hashed against those RPM-owned files,
not pristine source runtime; original tests/examples/config bytes are preserved.
Mypy is a build/test-only dependency; installed smoke retrieves it through the
protected bounded official repository transaction, not a runtime Requires.

Upstream GHA explicitly has CPython3.11 functional tests. Its other interpreter
matrix/type-check interpreter lanes and opt-in docs extras are not reproduced
or claimed; the strict command and example remain mandatory for this target.
No local candidate/backend/default/RPM/QEMU execution, target result, numerical
coverage, native RISC-V/performance, installed outcome, merge or publication is
claimed by proposal or trusted repository validation.

Historical distro discovery is lineage only: AUR1.6-4, openSUSE2.0-1.1 and
Debian/Ubuntu1.5.1 revisions are not substituted for current official sources.
Current full namespace/provider/closure and root literal review must pass
before commit; exact new-head CI/physical acceptance is separate.
