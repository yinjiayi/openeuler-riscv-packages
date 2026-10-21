<!-- SPDX-License-Identifier: Apache-2.0 -->
# Orderedmultidict 1.0.2

Target: openEuler 24.03 LTS SP3, riscv64/RVA23, locked QEMU user-mode image.
This pure-Python noarch RPM still requires actual target build/install evidence.

The canonical component is `github.com-gruns-orderedmultidict`, discovered
through the existing Arch/Debian/openSUSE snapshot. Distribution recipes were
not executed. Official PyPI reports stable 1.0.2; the latest Git tag 1.0.1 is
older and is not substituted. Source0 is the content-addressed PyPI sdist
SHA-256 `16a7ae8432e02cc987d2d6d5af2df5938258f87c870675c73ee77a0920e6f4a6`.

That sdist omits tests. Source1 is the official immutable Git archive at
`901194bed9c2de9e336358f3328132a81a14314e`, SHA-256
`cfa41406dd9428bb70c8d131206134cff0fe561a3cc94dd733795849e31d4c89`.
All four runtime files, setup.py, MANIFEST.in and LICENSE.md match the release
byte-for-byte; %prep enforces this again before copying the two original
test modules. Neither archive is committed to Git. No patch is needed.
The complete upstream Unlicense and author notices are retained in source,
SRPM and binary RPM; both original test modules carry the same notices.

Build is an offline, non-isolated setuptools wheel using target Python3.11,
setuptools68.0.0, wheel0.40.0 and pip23.3.1. Runtime requires six>=1.8.0;
the target supplies1.16.0. Setup tests_require flake8 is supplied unchanged.
Full official/supplemental primary/filelists preflight found no package,
Python distribution/module-owner, reverse dependency, managed-directory or
open-PR identity conflict. Preflight is not a target DNF transaction proof.

%check preserves upstream's documented `python3 setup.py test` RunTests
frontend. It discovers the entire original functional suite. Staged and
installed checks additionally require all55 original unittest cases with
zero skips/expected failures, unchanged test/runtime hashes and exact
distribution version/import provenance. The source runtime is absent during
the staged check; the installed smoke uses an isolated interpreter and fresh
test directory, with no source/fallback installation. This tests linked-list
and mapping behavior, multi-value update/pop, parity and binary operators.
It is not timing/performance, other-interpreter, legacy tox/nose matrix,
lint/type-check or native-hardware evidence. The target has no nose package;
upstream's separately documented unittest frontend needs only standard
unittest and six, and none of the original functional tests are removed.

Automatic updates are disabled until shared tooling can bind a PyPI release
to its matching supplemental original tests without selecting the stale Git
tag. Future versions require manual source/test pairing and full CI review.
Initial status is unknown: no local backend, upstream test, RPM or QEMU build
was performed. Exact-head CI/default test/install/physical RPM/SRPM acceptance,
explicit squash merge and public publication remain separate pending gates.
