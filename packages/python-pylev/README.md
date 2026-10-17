<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-pylev

This directory packages upstream `https://github.com/toastdriven/pylev` version `1.4.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Source and license

Source0 is the official PyPI 1.4.0 sdist, fixed by SHA-256
`9e77e941042ad3a4cc305dcdf2b2dec1aec2fbe3dd9015d2698ad02b173006d1`.
The release tag `v1.4.0` resolves to commit
`06760f3a5e40aa284cb8077762f630f1df210698`. All five module files, LICENSE,
README, setup.py and pyproject.toml match their complete Git blobs. PyPI adds
egg-info and normalizes setup.cfg; those changes do not alter test defaults.
The full BSD-3-Clause LICENSE is installed unchanged. The upstream release
commit is unsigned; exact official source hashes and Git identities are
recorded, not represented as publisher signature verification.

## Complete default and installed tests

The original release `.travis.yml` runs `python tests.py`; README also describes
`python -m unittest tests`. PyPI omits that file, so Source1 retrieves the whole
unchanged file from the same fixed commit, with SHA-256
`c5b78b0597aec0780a28547b690dd2f7d9fe2cc9a65c6d9f463dca8f9e9a6386`
and Git blob `b874256769632db2d68026437e4e79e3a9ee22b5`.
It generates 21 Levenshtein cases and one Damerau-Levenshtein case. The original
comment disabling the slow classic implementation is retained; no test is
removed or newly skipped. `%check` runs the exact original full default.

An installed test means the same whole suite is run against the installed
RPM-owned module, not a source-tree import. The smoke test verifies version,
RPM ownership and Source1 checksum, copies only the original test to a fresh
temporary directory, unsets PYTHONPATH, and repeats `python3 tests.py`.

## Target dependencies and status

The backend requires setuptools >=42 and wheel. The complete target metadata
supplies Python 3.11.6, setuptools 68.0.0 and wheel 0.40.0; stdlib unittest needs
no additional test dependencies. There are no package runtime dependencies
other than Python. The RPM is python3-pylev and provides python-pylev; canonical
inventory/open-PR and target namespace checks found no matching provider.

No RISC-V patch is justified: the source is architecture-independent Python,
with no native extension or architecture-specific code. Target build,
installation and suite execution remain pending remote CI. Static review and
source verification are not build success. No local upstream/backend/default
test/RPM/QEMU execution was performed during preparation.
