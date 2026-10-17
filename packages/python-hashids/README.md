# python-hashids 1.3.1

Hashids maps nonnegative integers to reversible short identifiers, with salts,
custom alphabets and minimum lengths. It is not cryptographic encryption.

## Canonical release and source

Official [PyPI](https://pypi.org/project/hashids/1.3.1/) still identifies 1.3.1 as
the latest stable release. Official
[v1.3.1](https://github.com/davidaurelio/hashids-python/tree/v1.3.1) points to
`138a12e85d09e7e76eebc1d0e059b2e28ba488e6`.
The complete commit archive SHA-256 is
`534d04f6902e2adb074f7cc4db227f1c2abebf88bb2c8470464ef0b2e5c83bc2`.
All ten source file identities match that official Git tree, with no symlinks,
hardlinks or traversal paths. No detached upstream signature was supplied.
The original MIT LICENSE and copyright notices are retained as RPM license data.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` retains the exact
`github.com-davidaurelio-hashids-python` component with Debian stable
`1.3.1-5`, openSUSE `1.3.1-1.29`, and Ubuntu `1.3.1-5build1` lineage. These are
discovery records, not source-byte proof. Stale AUR, PostgreSQL and Django rows
are excluded. No catalog or other package directory is changed.

## Target and default tests

Fixed target: openEuler 24.03 LTS SP3, riscv64, RVA23, locked OCI digest from
`ci/image.lock`. The RPM payload is architecture-independent Python.
Fresh official metadata provides Python 3.11.6, flit-core 3.8.0, pip 23.3.1 and
pytest 7.4.4, satisfying upstream's flit-core `>=2,<4` and pytest `>=2.1.0`.
Full official and current supplemental names/Provides/filelists have no hashids
provider or conflicting top-level module/distribution namespace. Supplemental
HTTP state/metadata binding is admission evidence, not fleet trust or publication.

The wheel uses the original flit_core PEP 517 backend with no network or build
isolation. `%check` preserves `.travis.yml`'s `python -m pytest` entrypoint,
unfiltered, adding only JUnit reporting. All 60 original tests are required:
33 modern API tests and 27 legacy alias tests, including salts, alphabets,
minimum lengths, integer/hexadecimal round-trips and invalid input. Installed
smoke repeats all 60 unchanged tests from RPM data against the installed module,
requiring zero failures, errors or skips. Pytest is an explicit runtime dependency
for that installed acceptance suite. No timing, hardware or native-kernel tests
are involved; no upstream test, feature or assertion is disabled.

No source patch is needed. Packaging code is repository-authored Apache-2.0;
upstream source remains MIT. Local validation covers repository/schema/source
checks only: upstream code, its backend/tests and RPM/QEMU are not run locally.
RISC-V status stays `unknown` until exact-head target CI and artifacts pass.
No RPM/SRPM publication or build-success claim is made by onboarding.
