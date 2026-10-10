<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-shortuuid

This directory packages upstream `https://github.com/skorokithakis/shortuuid` version `1.0.13` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Immutable source and provenance

Official stable `v1.0.13` resolves to commit
`16374d288c796faa2aee5789ed649c3ed7cdd9be`. Source SHA-256 is
`487c8d6094d3a7bc71a823fadcef6ff5efdbee13921f274da333870e45d6d438`;
all 19 regular archive members match the fixed Git tree. Retain the full
BSD-3-Clause `COPYING` notice (Stavros Korokithakis, 2011), original source
and original Poetry backend. No patches or external code were imported.

The actual merged non-stale component `github.com-skorokithakis-shortuuid`
from `discovery-20260808T165000Z-9a89920c269462cd` retains four original
AUR, Debian, Fedora and openSUSE source rows. Their observed distro versions
are historical provenance, not fresh source verification. AUR was not executed.

## Namespace and offline build

Source RPM: `python-shortuuid`; installable RPM: `python3-shortuuid`; Python
namespace and command: `shortuuid`. Complete primary and filelists scans cover
all 18,503 official RVA23 and 1,192 supplemental RPMs, hash/size-bound to fresh
repomd/state. No normalized provider, reverse dependency or namespace/command
owner matches shortuuid. Supplemental unsigned HTTP metadata is collision
evidence, not runner or repository trust recovery.

Official dependencies are Python 3.11.6, pip 23.3.1, poetry-core 1.4.0,
pytest 7.4.4 and wheel 0.40.0. Pip builds using upstream Poetry with
`--no-build-isolation --no-deps --no-index`, then installs only the resulting
wheel into RPM buildroot. The core library and original tests use stdlib only.

The optional `shortuuid.django_fields` adapter is retained unchanged, not
imported by the core package, and not a declared base dependency upstream.
Users of that adapter must separately supply compatible Django. No Django
provider was found in the audited repositories; this PR does not claim to
validate the adapter or provide Django. It does not remove the module or
suppress RPM dependency generation.

## Tests and version boundary

`%check` retains all 19 unchanged unittest cases selected by current upstream
`.github/workflows/test.yml` through complete default `pytest -v -q` collection.
No filters, skipped cases, coverage changes or timing thresholds are introduced.
Installed smoke runs the same entire module via unittest, then verifies the
installed distribution version and command-line encode/decode.

Upstream's pytest-action adds `--md` and `--emoji` for Markdown/emoji reports.
The reviewed plugins implement reporting hooks, not collection or assertions;
those presentation-only plugins are not required for RPM test output. A separate
pre-commit workflow runs source-mutating formatting and style/type authoring
hooks, which this RPM does not claim to replicate. Legacy tox/Travis and README
setup.py examples are stale: the fixed release has no setup.py and declares
Poetry. This is complete upstream runtime-suite preservation, not a claim that
every upstream authoring CI job is replicated.

The release/tag/Poetry distribution version is `1.0.13`, while upstream's
`shortuuid.__version__` constant is still `1.0.11`. Both are explicitly checked
as supplied; distribution metadata defines the package version. The constant
is not patched or reported as 1.0.13.

No local upstream/backend/test/RPM/QEMU execution was performed. Repository
validation and source verification do not establish target build success;
exact-head riscv64 build/install/smoke and physical artifacts remain CI gates.

## Duplicate wheel-license packaging repair

[The initial CI run](https://github.com/yinjiayi/openeuler-riscv-packages/actions/runs/38071774458)
for head `3a0d99d15396225db1c9c146ec6fbcc0011ac34b` built and installed the
original Poetry wheel and passed all 19 upstream runtime cases, but RPM's
final file check rejected an unowned `/usr/lib/python3.11/site-packages/COPYING`.
The wheel includes the original license at that generic root path. `%install`
now requires the redundant installed file to be regular and not a symlink,
compares its bytes with the unchanged original `COPYING`, and removes only
that equal duplicate. The complete original `COPYING` remains packaged by
`%license`; no global site-packages license path is claimed or upstream file
modified. Build dependencies, backend, default tests and smoke are unchanged.

The earlier `find: debug: No such file or directory` was nonfatal: subsequent
tests and file processing ran. The stored first-error summary selected that
noise; the terminal unpackaged-file error is the repair's causal evidence.
The failed head's install smoke did not execute. This packaging-only change
still needs replacement exact-head CI and physical RPM/install verification;
passing tests in a failed build is not RPM build or publication success.
