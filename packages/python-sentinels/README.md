<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-sentinels

Packages official Sentinels 1.1.1 as `python3-sentinels` for openEuler 24.03 LTS
SP3, riscv64/RVA23. This pure-Python library uses named singleton objects as
special values; it needs neither a native extension nor a native RISC-V runner.
Target build, installation, and smoke results remain pending CI.

## Source and license evidence

The fixed official [PyPI sdist](https://files.pythonhosted.org/packages/6f/9b/07195878aa25fe6ed209ec74bc55ae3e3d263b60a489c6e73fdca3c8fe05/sentinels-1.1.1.tar.gz)
is 4393 bytes, SHA-256
`3c2f64f754187c19e0a1a029b148b74cf58dd12ec27b4e19c0e5d6e22b5a9a86`.
[PyPI metadata](https://pypi.org/pypi/sentinels/1.1.1/json) binds the filename,
size, digest, non-yanked stable version, and official vmalloc/sentinels homepage.
All 11 original archive files (11933 bytes) were read as inert text, including
the full BSD-3-Clause grant in `LICENSE` (Rotem Yaari, 2011). `%license LICENSE`
retains its notice and redistribution conditions. Repository Apache-2.0 covers
only original packaging, not upstream code.

The available [PEP740 publisher attestation](https://pypi.org/integrity/sentinels/1.1.1/sentinels-1.1.1.tar.gz/provenance)
was cryptographically verified on 2026-10-09 with PyPA `pypi-attestations` 0.0.30
and Sigstore 4.5.0 production trust, without unsafe trust or time overrides.
Verification binds this exact sdist digest to `vmalloc/sentinels`, workflow
`ci.yml@refs/tags/1.1.1`, OIDC issuer `https://token.actions.githubusercontent.com`,
and source commit `232ae4d7d2d885f02006153558ffb7ba479779ef`.
Reproduce with `pypi-attestations verify pypi --repository
https://github.com/vmalloc/sentinels sentinels-1.1.1.tar.gz`. This is a keyless
attestation, not an OpenPGP signature: `sources.yaml` has no fabricated public-key
fingerprint. CI independently verifies the committed SHA-256 before RPM build;
it does not implement automatic PEP740 verification.

Discovery lineage is frozen in
`discovery-20260808T165000Z-9a89920c269462cd`, `/rejections/155859`, canonical
`github.com-vmalloc-sentinels`: Arch 1.1.1-2, Debian 1.0.0-8, and Fedora
Everything-source 1.1.1-2.fc44. These are discovery inputs, not executed recipes.
Full historical PR files plus a fresh delta, current main, target primary
providers, and complete target filelists were checked for aliases/ownership.

## Build and validation contract

The official target repository provides Python 3.11.6, pip 23.3.1, wheel 0.40.0,
hatchling 1.27.0, hatch-vcs 0.3.0, pytest 7.4.4, and pylint 3.0.3. Upstream
requires Python >=3.9 and hatchling >=0.25.1; there are no external runtime
dependencies. Dependency preparation happens before an offline build. The
pinned sdist's `PKG-INFO` supports hatch-vcs version resolution without Git or
network. Wheel build uses `--no-build-isolation --no-deps` and `PIP_NO_INDEX=1`;
installation uses only the locally built wheel.

`%check` preserves both unfiltered upstream CI commands: `pytest -v tests`
(the README doctest test) and `pylint --rcfile=.pylintrc sentinels tests`. It does
not suppress lint errors or remove tests. Installed distribution metadata is
available through the buildroot Python path because upstream `__version__`
uses `importlib.metadata`. The installed smoke runs Python isolated from the
source tree and checks version, singleton reuse, equality, shallow/deep copy,
all supported pickle protocols, and legacy `obj_id` compatibility.

No local upstream code, RPM build, or QEMU execution was performed. Static
repository validation and source-only verification are not target build success.
No patch is currently required; any real target failure must be assessed from
exact-head CI before changes. RPM/SRPM and publication links will be added only
after actual verified artifacts exist. Auto-merge is disabled; protected-main
merge and package publication remain subject to the repository trust gates.
