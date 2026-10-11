<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-sexpdata

This directory packages official stable sexpdata 1.0.2 for openEuler 24.03 LTS
SP3, Python 3.11, `riscv64`/RVA23. A source recipe is not target build, installed
test or publication success; these remain pending.

Source0 is official tag `v1.0.2`, fixed commit
`29170a5daed7c07a8d035856356416141210d963`, SHA-256
`71ce6783d7081337df493c660c54b3b62651493a35f3e37425f74a31801f929c`.
All 22 Git blobs remain unchanged, including module, tests, both CI workflows,
pyproject.toml, setup.py, tox.ini and Makefile. Latest official PyPI stable is
also 1.0.2, sdist SHA-256
`92b67b0361f6766f8f9e44b9519cf3fbcfafa755db85bbf893c3e1cf4ddac109`;
all shared original files match the tag archive. Generated PyPI metadata is not
overlaid. GitHub API reports the fixed commit's signature verified (`valid`),
not local PGP verification of archive bytes. Sources have full SHA-256 binding.

The applicable default suite is the current official
`.github/workflows/tests.yaml` Python 3.11 entry:
`pytest --doctest-modules sexpdata.py test_sexpdata.py`. The complete unchanged
command is retained in `%check`; the equivalent `python3 -m pytest` selects the
supplied Python interpreter, not a different suite. All unit tests and both
module/test doctests remain, including original doctest skip annotations.
There are 23 statically counted test definitions, not an observed runtime test
or passing count. No new skip, filter, failure suppression or source patch is
introduced. Other Python/OS matrix members are unverified.

Installed smoke checks version, installed module path and RPM ownership from
a new scratch directory with PYTHONPATH unset. It copies only the complete
unmodified RPM-owned test file there, never the source library, then executes
the same full pytest/doctest command with the absolute RPM-owned installed
module path. Thus the module doctest collection and unit-test imports target
installed library bytes, not a copied source-module substitute.

Alternate original developer routes remain unchanged in Source0: tox.ini
runs the same full suite but additionally provisions `pudb`; Makefile `test`
calls tox and can regenerate the checked-in module via `cog.py`. Historical
Travis calls tox. Current official GitHub workflow directly invokes pytest,
not tox or make; these alternate developer routes are not the applicable
Python 3.11 workflow gate and are not claimed executed or supplier-closed.
The complete target metadata has no pudb/cogapp supplier. Requiring those
alternate routes would first require separately reviewed target suppliers;
their absence does not establish a failure of the current full default suite.
Documentation and benchmarks are separate development targets, not original
current-workflow test steps; no documentation/benchmark success is claimed.

The original unversioned setuptools.build_meta/setup.py backend has no target
Python 3.11 runtime dependencies beyond the standard library. Its historical
singledispatch import is a fallback only when standard-library functools lacks
it, not a target dependency. Supplied Python 3.11.6, setuptools 68.0.0 and
pytest 7.4.4 close this recipe. Complete official/supplemental primary and
filelists scans (18,503/1,192 packages in each respective document) found no
sexpdata provider, module owner or reverse dependency. This is static supplier
evidence, not an executed dependency transaction or target test result.

The original complete `LICENSE` contains Joshua Boyd's 2019 BSD 2-Clause
notice; original `sexpdata.py` contains Takafumi Arakaki's complete 2012 BSD
2-Clause notice. `%license LICENSE sexpdata.py` ships both original full files,
also preserving the source notice in the installed module. No license text
or module is rewritten and no additional source/patch is introduced.

Four frozen discovery lineages (AUR 1.0.2-3, Debian 1.0.2-1, Fedora
1.0.2-9.fc44, Ubuntu 1.0.2-1build1) remain historical records. Current official
source verification resolves their `unverified-upstream` discovery decision,
not a claim that frozen versions are live distro state. Canonical upstream is
`github.com-jd-boyd-sexpdata`; live GitHub API resolves old `tkf/sexpdata` to
the same repository. RPM payload name is `python3-sexpdata`, while the package
directory/discovery name is `python-sexpdata`.

Preparation uses only trusted repository validation and source-only/inert
inspection, never local upstream import/backend/pytest/default/RPM/QEMU.
Package metadata requests no build network; current shared build configuration
enables container network. Cache-only verified source reuse does not prove a
disconnected container. No successful build, artifact URL, publication or
runner trust restoration is claimed.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
