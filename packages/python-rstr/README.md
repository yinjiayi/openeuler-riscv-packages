<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-rstr

Packages Rstr 3.2.2 for openEuler 24.03 LTS SP3, riscv64/RVA23.
The official tag `3.2.2` resolves to `231837460e6eb5522884117dc38311a374b36012`;
`sources.yaml` pins this fixed archive and SHA-256. The complete BSD-3-Clause
`LICENSE.txt`, including the Leapfrog Direct Response LLC copyright and
endorsement condition, is retained. No upstream signature is claimed.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Upstream CircleCI invokes tox: every interpreter environment runs complete
`python -m unittest` discovery, and its typing environment runs
`mypy --strict rstr`. This recipe preserves both whole gates, all four test
files, `pyproject.toml`, `tox.ini`, and the typed marker without patches,
new ignores, skipped cases, or narrowed test selection. The locked target
is Python 3.11, not evidence for tox's other interpreter environments.

`tox.ini` pins mypy 1.6.0 for upstream development. Target mypy 1.10.0 is
used with the unchanged strict command. Static review covers all three
library modules, target strict flags and import-not-found error code, and
typeshed inventory: the original Python 3.11 `re._parser` import still has
no supplied stub, while the older-Python `sre_parse` fallback is unchanged.
This is a development-tool compatibility boundary, not successful typecheck
evidence: CI must run the complete strict gate. Hard backend requirements
setuptools >=61.2, wheel, and setuptools_scm[toml] >=3.4.3 are satisfied by
target metadata. The official release version uses target setuptools_scm's
supported `SETUPTOOLS_SCM_PRETEND_VERSION_FOR_RSTR` for the Git-less archive.
Target wheel 0.40.0 clamps ZIP timestamps to 1980, including epoch-zero
inputs; no timestamp patch is introduced.

Installed acceptance verifies RPM ownership and byte equality of all typed
reference files against the installed library. Complete unittest discovery
runs in a writable directory containing only tests/config, with no source
library shadow. Strict mypy then runs on the reference in a separate
directory; the reference is static input, never the imported runtime library.
Mypy is a dependency for installed acceptance, not upstream runtime use.

Local checks are this repository's validation/tests/golden and offline source
verification only. RPM build, original unittest, strict typing, installation
and riscv64 acceptance remain CI gates. Status stays unknown until matching
complete CI and physical artifacts are verified.
