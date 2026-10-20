<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-expandvars

Packages official stable Expandvars 1.1.2 for openEuler 24.03 LTS SP3,
`riscv64`/RVA23. Official `v1.1.2` resolves to
`bfdd3f6cf86934f2c3318dd949676aa382be4a89`; full Git source archive SHA-256 is
`93e107354379d3fa7a04e1ce7451d1c9d0c4a9442850c730eedcea32260b290d`.
All Git blobs were verified against the recursive tree. No upstream release
signature is used: HTTPS and SHA-256 are not GPG proof. Full MIT license
remains upstream's; original packaging is Apache-2.0.

The pure Python library has no runtime dependencies. Build uses supplied
Hatchling and installs its wheel with pip offline/no-dependency mode.
Black, pytest and pytest-cov are installed-suite support, not upstream runtime
dependencies. Full target primary/filelists and complete open PR files are
screened for canonical names, module owners and reverse requirements.
This is static admission, not a DNF transaction result.

The **default acceptance contract** is the original `tox.ini` sequence,
all four original pytest files, initializer and text fixture, with unchanged
`pyproject.toml` and coverage configuration:

```
black --diff .
pytest --cov --cov-report=html --cov-fail-under=100
```

Original Black is a diff diagnostic, not a formatting check, and stays
unchanged. Hosted CI runs the same whole pytest suite with the 100% threshold.
Codecov upload is hosted report transfer, not an offline RPM test. `uv.lock`
is preserved but the original pip/tox workflow does not use it to resolve
dependencies. No default tests or thresholds are dropped; no patch is needed.

`%check` tests the whole source suite. Installed acceptance verifies ownership
and version of the imported `/usr` module, then repeats the original whole
contract in a fresh writable directory with all RPM-owned fixtures/config.
A byte-identical source under `reference/` is lint input only and cannot
shadow the installed library; no module copy exists at scratch root.

Local verification runs trusted repository tests and offline source-only
checks, not upstream/backend tests or RPM/QEMU builds. CI must independently
prove full source tests, installed suite and physical RPM/SRPM products for
the exact current head before merge/publication.
