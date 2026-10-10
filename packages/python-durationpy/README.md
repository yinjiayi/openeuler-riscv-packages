# python-durationpy

Durationpy converts Go duration strings to and from Python `datetime.timedelta`.
The source package is `python-durationpy`; its noarch runtime RPM is
`python3-durationpy`. No RPM or public repository URL is claimed here.

## Official release and discovery

Release 0.11 is the current non-yanked stable release observed through
<https://pypi.org/pypi/durationpy/json>. The official repository is
<https://github.com/icholy/durationpy>. Frozen discovery snapshot
`discovery-20260808T165000Z-9a89920c269462cd`, row `/rejections/132913`, retains
canonical `github.com-icholy-durationpy` with Arch 0.10-2, Fedora Everything
source 0.9-8.fc44 and openSUSE 0.10-1.4 lineage. These older versions are
discovery lineage, not substituted executable packaging or claimed release 0.11.
Current-main, complete all-state PR history plus a fresh delta, and all 18,503
official target primary/filelists entries were checked for aliases/providers and
the durationpy module/dist-info namespace; no owner or PR collision was found.

The primary source is the complete official fixed release-commit archive:

- Tag: `0.11`; commit: `3df7a337a852f0b432f73c4892c4b48590a01bd0`.
- URL: <https://codeload.github.com/icholy/durationpy/tar.gz/3df7a337a852f0b432f73c4892c4b48590a01bd0>.
- Local filename: `durationpy-0.11-official.tar.gz`; size: 4,666 bytes.
- SHA-256: `30b03223035e7902b388bedad81ed2837eac066abdd105c378a9e49a50166838`.

All 13 original regular files were reviewed inertly, including the complete
test.py, workflow, setup.py, type stubs, MIT license and development metadata.
The PyPI sdist has SHA-256
`181898e1ae282e288f0a2291829656bf1b6b3aadf30a97993b85db4943642905`
but omits test.py. It is corroborating release evidence, not the testless build
input. Seven overlapping source/license/docs/stub files match exactly; its
generated setup.cfg adds an egg_info section to the original metadata section.

## Signature and license boundary

The available original SSH commit signature was independently verified with
`ssh-keygen -Y verify`, namespace `git`, signer `ilia.choly@gmail.com`. The exact
signature public key matched the current official icholy account signing key
returned by <https://api.github.com/users/icholy/ssh_signing_keys> over verified
HTTPS. No arbitrary keyserver key or signature-policy override was accepted.
The signed payload's tree, all recursive Git tree objects, every blob's original
bytes/mode/path, and the complete folded-signature Git commit object were
independently reconstructed and matched the pinned commit/tree identities.
Git object SHA-1 identifies upstream Git objects; retained archive/file bytes
also have SHA-256. This verifies the signed commit and bound source tree, not a
separate signature over the PyPI sdist. Its PyPI PEP740 provenance endpoint
returned HTTP404; no PyPI attestation is claimed.

`sources.yaml` has `signature: null` because its signature object represents
OpenPGP fingerprints, not SSH commit verification. Admission verified SSH
separately; target source-only verification enforces the fixed archive SHA-256
and does not claim to rerun that SSH verification.

The full 1,050-byte original MIT LICENSE grants redistribution subject to
retaining Copyright 2017 Ilia Choly and the entire permission/warranty notice.
`%license LICENSE` preserves the original grant and `%doc README.md` the original
documentation. Original files are not patched or replaced. There is no runtime
external dependency beyond Python's standard library `re` and `datetime`.

## Target build and default test

The target remains openEuler 24.03 LTS SP3, riscv64, RVA23 using the repository's
locked image. BuildRequires python3-devel 3.11.6, setuptools 68.0.0, wheel 0.40.0
and pip 23.3.1 have official target providers. No upstream minimum backend
constraint is relaxed. Upstream mise's `python setup.py sdist bdist_wheel` is
retained, without dependency fetching; pip installs only its local wheel using
no-index/no-deps and the target build phase has no network. Twine/uv are release
upload/developer tooling, not required by the original default test/build.

A deterministic ZIP epoch floor means unset SOURCE_DATE_EPOCH is treated as
zero and nonnegative decimal epochs before 315532800 (1980-01-01 UTC) are raised
only to that minimum. Later values retain their original representation;
empty/negative/nondecimal values fail closed. Leading-zero stripping is only
for comparison and length checks avoid shell integer overflow. Very large later
values can still fail downstream timestamp limits. This is ZIP compatibility,
not a claim about release date or arbitrary timestamp support.

`%check` runs the exact original `python test.py`: two unittest methods looping
the original 50 parser/formatter case rows, including signs, microsecond
precision, invalid values and range errors. No test filtering, skip injection,
source modification or reduced substitute suite is added. These are duration
arithmetic tests, not wall-clock performance or privileged/native-only tests.
Target Python3.11 is within the original 3.9/3.10/3.11 CI matrix; this recipe
does not claim all matrix interpreters ran. The independent installed smoke
uses `/tmp` and `python3 -I` to check installed version/import location,
parse/format round trips, sign, precision, extended units and error behavior.

Local validation is limited to repository tooling, schema/source verification
and inert static review. No downloaded code/backend, RPM or QEMU build runs
locally. Full exact-head CI must prove target build, unchanged default tests,
installation, smoke and actual RPM/SRPM products before target success is
claimed. Main merge, trusted-fleet acceptance and public publication are
separate gates; no auto-merge is enabled.
