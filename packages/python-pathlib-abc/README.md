<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-pathlib-abc

This noarch recipe packages the official pathlib-abc 0.5.2 release for openEuler
24.03 LTS SP3, riscv64/RVA23. The source package is `python-pathlib-abc`; the
installed binary package is `python3-pathlib-abc`. It supplies abstract base
classes for pathlib-like virtual filesystem paths, not a filesystem server.

## Source identity, signature and license

Discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`, frozen row
`/rejections/121012`, canonical component `github.com-barneygale-pathlib-abc`,
retains AUR 0.5.2-1 and Fedora Everything-source 0.5.2-2.fc44 lineage. These are
discovery evidence, not borrowed or executed distro packaging.

Official identity: <https://github.com/barneygale/pathlib-abc> and
<https://pypi.org/pypi/pathlib-abc/json>. The fixed 33,342-byte sdist is:

<https://files.pythonhosted.org/packages/d6/cb/448649d7f25d228bf0be3a04590ab7afa77f15e056f8fa976ed05ec9a78f/pathlib_abc-0.5.2.tar.gz>

SHA-256: `fcd56f147234645e2c59c7ae22808b34c364bb231f685ddd9f96885aed78a94c`.
All 32 regular files, totaling 162,039 bytes, were read as inert text. No
archive symlink/traversal/native-extension source or upstream execution.

PEP 740 is PyPI's signed publisher-provenance evidence, not an RPM signature.
Official provenance at
<https://pypi.org/integrity/pathlib-abc/0.5.2/pathlib_abc-0.5.2.tar.gz/provenance>
was verified with PyPA pypi-attestations 0.0.30 and Sigstore 4.5.0 production
trust, no staging/offline trust overrides. Exactly one attestation bound this
archive digest to issuer `https://token.actions.githubusercontent.com` and
certificate identity
`https://github.com/barneygale/pathlib-abc/.github/workflows/build.yaml@refs/tags/0.5.2`;
source commit `44506435e7924f24bb8b0d84d088b3a133c3396a`. Reverification must
enforce this exact identity and archive digest, not only the repository name.
The repository sources schema encodes OpenPGP fingerprints only, so its
`signature: null` cannot encode this verified keyless evidence. Target source
verification independently enforces the pinned SHA-256; it does not claim to
rerun the keyless verification.

The original full eight-clause PSF-2.0 LICENSE.txt grants redistribution with
retention of the PSF copyright and agreement and a changes summary for
derivatives. `%license LICENSE.txt` and `%doc CHANGES.rst README.rst` retain
those original materials. No upstream changes or RISC-V patches are proposed;
`patches/series` is empty.

## Build, tests and ownership

Build dependencies are python3-devel, python3-pip, python3-wheel,
python3-hatchling and python3-pytest; runtime requires Python >=3.9, with no
external Python runtime distribution. Official target primary metadata and
all 18,503 filelist package records were completely checksum-verified.
Python 3.11.6 is supported by the upstream matrix. Target `python3` owns the
stdlib `test/support/__init__.py` required by the original suite; official
CPython v3.11.6 source inspection confirms `load_package_tests`'s original
four-parameter API. No invented separate `python3-test` package is required.
No existing target package/provider or pathlib_abc namespace ownership was
found, and current main plus the complete historical PR snapshot and a fresh
all-state increment were checked for canonical/alias collisions.

Dependency preparation occurs before the target's offline build. pip wheel
uses the original hatchling backend with no index, dependency download or
build isolation; only the locally produced wheel is installed into buildroot.
A deterministic ZIP epoch floor means raising unset/earlier nonnegative ASCII
decimal SOURCE_DATE_EPOCH values to 315532800 (1980-01-01 UTC), the minimum
wheel ZIP timestamp. Later values retain their representation. Empty, negative
or nondecimal values fail closed; leading zeroes are stripped only for
comparison and large values avoid shell integer overflow. Later values may
still exceed downstream date limits. This is not a release-date/provenance
claim. The package-local shell logic follows this repository's independently
reviewed Sentinels epoch repair, preserving upstream bytes and default tests.

`%check` preserves upstream tox's entire `pytest tests` command and
`PYTHONWARNDEFAULTENCODING=1`, with no selection/filter or added skip. The
original `tests.support.is_pypi = True` selects the distributed backport suite;
stdlib comparison branches disabled by upstream are not falsely claimed run.
Original platform/symlink skips remain as upstream authored. `%check` exercises
the original source tree, not installed-code proof. The separate installed
smoke runs from `/tmp` with `python3 -I`, excludes source/CWD/user PYTHONPATH
shadowing, and checks installed distribution version, ABC relationships,
lexical path derivation/relative paths/glob matching and vfsopen round trips.
Only pathlib_abc and its dist-info are installed as runtime modules; test and
documentation helper packages are not installed.

## Validation boundary and next action

Local work is source-only/static tooling validation. No local upstream,
hatchling backend, RPM/QEMU or installed candidate execution is permitted.
Target build, complete default pytest results, actual installation/smoke and
physical RPM/SRPM evidence must come from this PR's exact-head hosted CI.
No build success, artifact URL, auto merge, main merge or public publication
is asserted here. Fast-copy syscall features do not by themselves establish a
native-only requirement; classify actual target limitations from real CI.
Protected main merges and public package publication retain the repository's
trust hold. The next acceptance gate is complete exact-head target evidence,
independent of continuing admission of the next distinct package.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
