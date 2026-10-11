<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-python-lorem

This directory packages upstream `https://jarryshaw.github.io/lorem/` version `1.3.0.post3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The canonical project is JarryShaw's `python-lorem`, not other projects which
share the word lorem. The frozen AUR lineage calls it `python-python-lorem`;
the binary RPM is `python3-python-lorem` and the import is `lorem`.
Source0 is the official stable `v1.3.0.post3` tree at
`04b9e25393906e45e1894b1c63a62e0224a370c7`, SHA-256
`c834126c40dba599ae2584d9c7c51d5e8ba5a7548ba2b4d198fa252219065d69`.
All 44 Git blobs, full BSD-3-Clause LICENSE, original test and coverage
configuration were checked; neither distro recipes nor upstream code ran locally.

A build-command compatibility patch fixes the unconditional import of
`setuptools.command.bdist_wheel`, absent from target setuptools 68.0.0.
Only that exact missing-module exception falls back to the audited wheel
0.40.0 command; unrelated import errors still propagate. It changes no
library or test logic, is not a RISC-V source fix, and is not sent upstream.
Remove it once upstream handles the import or the target provides that module.

The default test contract is the complete Python 3.11 upstream workflow's
`coverage run test_lorem.py`, including all ten original unittest methods and
unchanged `.coveragerc`. The target calls the identical entry point through
`python3 -m coverage` because its console script is named `python3-coverage`.
The installed-RPM gate checks version and ownership, copies only the complete
installed test/config to fresh scratch, and repeats that whole coverage run
against the RPM-owned library without source-directory or PYTHONPATH shadowing.
Cross-platform matrix runs, codecov upload, native hardware and performance
are not claimed. Target build and installed test success require CI evidence.

Checksum-bound current official primary/filelists and supplemental immutable
generation metadata show no exact RPM/Provides/module/test/egg-info conflict
or reverse requirement. Python 3.11.6, setuptools 68.0.0, wheel 0.40.0 and
coverage 7.3.2 are supplied. Physical wheel/coverage/setuptools payloads were
examined without installation; broad font/TeX/Perl name matches are unrelated.
