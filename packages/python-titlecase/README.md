<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-titlecase

Packages official Titlecase 2.4.1 for openEuler 24.03 LTS SP3, riscv64/RVA23.
The MIT-licensed release v2.4.1 resolves to commit
`418c57ca6c7f324ddc2813b3fc88d52e84db63bd`; the complete 12-blob Git tree is
pinned by source SHA-256 `16f0632e458ac8d24d7618fcd15f2b852db2314315a70e8fdaddda56d890b082`.
PyPI latest formal metadata corroborates version 2.4.1. The initial formal
sdist transport failed TLS; it is not used as an unverified source substitute.
No distribution recipe or upstream code was executed during intake.

Discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd` retains
Arch, Debian, openSUSE and Ubuntu metadata as lineage, not executable evidence.
The canonical component is `github.com-ppannuto-python-titlecase`; the
Python distribution is `titlecase`, RPM/package directory `python-titlecase`.

The original `pyproject.toml`, setup files, runtime, tests, tox and CI files are
unchanged. Offline wheel construction uses target setuptools >=46.1.0,
setuptools_scm >=5, wheel and pip. `SETUPTOOLS_SCM_PRETEND_VERSION=2.4.1`
supplies the verified tag version for the Git archive lacking `.git`; it does
not replace the backend, alter the original version scheme or change source.

Default-test acceptance means the whole original `python -m unittest` command,
not a selected case: 10 methods with 72 input/output fixtures. One original
upstream `unittest.skip` remains unchanged and is visible in test output; this
is not evidence that the skipped small-word-list case passed. Both original
CI modes are retained: installed optional regex and standard-library re.
A packaging-owned import blocker only makes the optional regex import absent
for the latter mode; no test or upstream runtime is patched. Coverage uses the
original `coverage run -m unittest` command in both modes. Remote coverage
uploads are telemetry, not an offline functional acceptance condition.
The target RPM supplies the same coverage entry point as `/usr/bin/coverage3`,
not unversioned `coverage`; an isolated scratch PATH alias preserves the
literal original command. Installed smoke verifies that provider's ownership.

The installed smoke gate verifies version, RPM ownership and all 12 original
source-file digests, then replays byte-identical whole tests from a fresh
tests-only root against the installed RPM library, without source shadowing.
No local upstream/backend/default test, RPM build or QEMU run was performed.
Static complete supplier namespace and dependency checks are admission
evidence, not a solved DNF transaction or successful riscv64 build. CI must
still verify offline build, full default gates, installation and smoke.

No patch is required. `patches/series` is empty. Packaging files are
Apache-2.0; original redistributed source snapshots retain MIT and original
copyright/contributor notices.
