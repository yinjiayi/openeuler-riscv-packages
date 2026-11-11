<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-pydash

Packages official Pydash 8.1.0 for openEuler 24.03 LTS SP3 riscv64/RVA23.
Source is the fixed upstream Git commit `f46de3669742c075e5379c1e193c86c1c2c70dc2` from
the official signed `v8.1.0` tag. GitHub records the tag signature as valid;
this is not a claim of an independently verified detached archive signature.
The codeload archive SHA-256 is `d7b227c8c4998fbd24858ed54f4adfc62b95d080bd513eebd379cb35caca5e23`.
All 76 original files and the full MIT notice are retained, with a per-file
SHA-256 manifest. The runtime preserves all 17 original package files,
including `py.typed` and `chaining/all_funcs.pyi`.

## Original default test scope

Both RPM `%check` and the installed smoke test run the unchanged upstream
`python3 -m invoke test` task against the actual wheel/buildroot or RPM-owned
site-packages. Upstream's original site relocation variable is used;
the pristine `pyproject.toml`, tests and task arguments remain unchanged.
That default task selects `src/pydash tests --cov=pydash` with only its
original `--ignore=tests/pytest_mypy_testing` exclusion. All core tests
(410 statically identified test functions; the parametrized/doctest count
must be measured in CI), module doctests and the original 100% coverage
threshold are retained. No new skip, filter, xfail or coverage exception is
added. The observer records results without changing them; the guard
verifies each candidate module's immutable origin and SHA-256, then unloads
only candidate modules after preflight so coverage measures subsequent
original imports. Installed mode verifies RPM ownership for runtime,
metadata, source payload and archive.

The upstream `inv ci` docs/lint steps, optional `--with-mypy-tests` mode and
whole tox interpreter matrix are separate scopes, retained but not claimed
as RPM default-test acceptance. The optional type-test plugin is not
imported by the original default conftest/core tests. Current static
supplier review selected Python3.11.6, setuptools68, wheel0.40, pytest7.4.4,
pytest-cov4.1, typing-extensions4.12.2 and Invoke2.2, with 118 packages /
935 static dependency edges and 21 reviewed non-EQ bounds. Static
capability closure is not DNF solving or a successful target build.

## One-line backend metadata compatibility patch

`patches/0001-license-file-metadata.patch` changes only upstream
`license = "MIT"` to `license = {file = "LICENSE.rst"}`. The fixed official
setuptools v68 validator accepts file/text license tables; PEP639 license
expression string support arrived in v77. The complete MIT notice,
`setuptools>=61.0`/wheel build-system contract, runtime dependencies and
all original default tests/configuration are unchanged. The pristine
source is copied before applying the patch and remains available in the
installed payload. This is a downstream metadata compatibility patch,
not a RISC-V source workaround or an upstream-submitted change. Remove it
once the verified target selected backend supports the original string
form (setuptools>=77).

Patch source is the [fixed original MIT pyproject](https://github.com/dgilland/pydash/blob/f46de3669742c075e5379c1e193c86c1c2c70dc2/pyproject.toml).
The header explicitly records that original MIT license, applicability
to upstream 8.1.0 / selected setuptools68, downstream-not-submitted status,
metadata-schema root cause and the verified setuptools>=77 removal condition.

Upstream references: [setuptools v77 history](https://setuptools.pypa.io/en/latest/history.html#v77-0-0),
[fixed v68 validator](https://github.com/pypa/setuptools/blob/v68.0.0/setuptools/config/_validate_pyproject/fastjsonschema_validations.py).
No local upstream/backend/default tests or RPM/QEMU build were executed.
Exact-head CI must still produce a real RPM/SRPM and pass build, install
and complete source/installed defaults; no target success or artifact URL
is claimed here. Upstream files remain MIT; original packaging is
Apache-2.0.
