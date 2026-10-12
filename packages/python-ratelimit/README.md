<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-ratelimit

Packages Ratelimit2.2.1 for openEuler24.03LTS SP3 riscv64/RVA23 at official
Git commit `1cddcbd9708cdab583551f0bc5a0d40d7ed2eaa3`, full archive SHA-256
`9ecb5a42d0206f234e2a568f246a2cb52b3aa1f54432d3e85839bb637db97f53`.
All15 original Git blobs are retained. Runtime, setup.py and MIT LICENSE
match the formal PyPI2.2.1 sdist; Git supplies omitted tests/default configs.
Frozen discovery license/staleness decisions are not current upstream evidence.
The repository Apache-2.0 license covers packaging only, not upstream source.

The original Travis command `py.test` and unchanged pytest.ini are used for
the complete suite: verbosity, doctest collection, original setup.py ignore,
term-missing and HTML coverage are preserved. All4 static unittest methods
use the original deterministic Clock; four is not a local test-pass claim.
No newly added test filters, skips, or coverage waiver is used.

Original requirements.txt retains pytest==2.6.4, pytest-cov==2.5.1 and
pylint==1.7.2. These are historical development pins, not install_requires;
Travis invokes py.test and has no pip-r step. The actual supplied target tools
are Python3.11.6, pytest7.4.4, pytest-cov4.1.0 and pylint3.0.3. They do not
satisfy the historical equalities. CI must verify this target compatibility;
no historical Python2.7/3.2 matrix or exact-pin environment success is claimed.

Installed smoke checks every original archive blob, all3 runtime modules and
all3 test-package files plus default config against fixed source hashes and
RPM ownership. Scratch tests see only an alias symlink to the RPM-installed
runtime, never a copied source runtime, so unchanged doctest collection still
visits every original runtime module. An import guard binds resolved runtime
paths to installed site-packages. The complete unchanged py.test default runs
again against that installed runtime. This proves neither native timing nor
performance; no backend/default/target/RPM/QEMU code was executed locally.

Static full supplier review covers18,503 official and1,205 supplemental
packages and125 dependency packages. The literal resolver's rich-OR isort row
is preserved in raw evidence; reviewed official isort5.12 satisfies its
`<5.13` alternative. This is supplier feasibility, not DNF transaction success.
