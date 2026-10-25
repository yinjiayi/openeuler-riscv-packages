<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-dpath

This directory packages the official stable dpath 2.2.0 release for openEuler
24.03 LTS SP3, Python 3.11.6, `riscv64`/RVA23. The source RPM is `python-dpath`;
the runtime RPM is `python3-dpath`, Python distribution/import name `dpath`.

## Source, lineage and license

Official `v2.2.0` resolves to commit
`c8722e6b815bedf4e6aaeea9ccc7d6ff3e9b4f84` in
<https://github.com/dpath-maintainers/dpath-python>. `sources.yaml` pins its
archive SHA-256 `651a30e79544b5cc65f9c4755643100096ffcddadbd228835281991b4110dc09`.
All 34 regular archive files match the Git tree's blob identities and sizes.
The stable PyPI 2.2.0 sdist agrees byte-for-byte on all 26 shared files;
its six additional files are generated setuptools metadata, not substituted
source. No upstream signature is advertised in the reviewed release metadata.

Frozen discovery `discovery-20260808T165000Z-9a89920c269462cd` retained AUR
and Fedora `python-dpath`, plus Debian and Ubuntu `dpath-python` clues.
Historical `akesterson/dpath-python` redirects to the official maintained
repository; the pinned source, setup metadata and stable PyPI release resolve
the formerly unverified-upstream/license-blocked clues. Only the actual four
Python lineage rows are carried forward; unrelated Perl Data::DPath and
similarly named components are not aliases. No distro recipe was executed or
copied.

The complete upstream `LICENSE.txt` is MIT, copyright 2013 Andrew Kesterson
and Caleb Case, and is installed with `%license`. Original packaging is
Apache-2.0; no patches are needed.

## Offline dependencies and namespace

The original setuptools `setup.py` is retained without a substituted backend,
version change or dependency relaxation. Upstream requires Python >=3.7 and
declares no third-party runtime dependencies. The official target provides
Python/devel 3.11.6, setuptools 68.0.0, pip 23.3.1 and wheel 0.40.0.
Build/test dependencies additionally include nose2 0.13.0, hypothesis 6.98.9
and flake8 7.0.0; their declared target dependencies include sortedcontainers
2.4.0, mccabe 0.7.0, pycodestyle 2.11.1 and pyflakes 3.2.0. CI resolves these
target RPMs before the offline wheel build/install phase.

Fresh pre/post repomd and supplemental-state binding covered all 18,503
official and 1,192 existing supplemental primary/filelists entries. No dpath
Python provider, reverse dpath dependency constraint or owned Python dpath
path was found. This readonly supplemental HTTP metadata check is not
independent build-machine trust recovery or publication acceptance.

## Original gates and installed smoke

`%check` retains the full original `nose2` default discovery, all 14 original
Python test files and hypothesis's original default profile/example settings.
It also retains the separate upstream CI flake8 exit gate over
`setup.py dpath/ tests/`, with the unchanged `tox.ini` E501/E722 ignores.
The referenced TrueBrain/actions-flake8 v2.3 action, resolved to
`a3b8724ab5391cc5869d9c746b4fd67b61710f20`, invokes the same flake8 paths
and fails on its exit status; no test filter or failure suppression is used.

The upstream workflow uses one shared randomly generated hash seed across
its Python matrix. This reproducible target recipe uses `PYTHONHASHSEED=1`
and does not claim to repeat that entire matrix. `tests/smoke.sh` independently
checks the installed distribution/version and typed-marker plus nested
get/values/set/new/delete/merge behavior. This installed API smoke is not the
full source-tree suite; that suite remains the mandatory `%check` gate.

No upstream/backend/tests or RPM/QEMU build was executed locally. Trusted
repository validation and verified-source-only materialization do not prove
target build success. Acceptance remains unknown until exact-head CI build,
installation/smoke and physical RPM/SRPM evidence is observed; no merge,
Auto-merge, native-RISC-V or public-release claim is made here.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
