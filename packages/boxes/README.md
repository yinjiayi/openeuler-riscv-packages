<!-- SPDX-License-Identifier: Apache-2.0 -->
# boxes

This directory packages the official stable boxes 2.3.2 release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The official GitHub tag resolves
to commit `cebddf7abf4d6a5e0846678263f9e420424b57bd`; its HTTPS source
archive is pinned by SHA-256. The archive has no absolute or traversal paths
or symlinks. Upstream's `LICENSE` and source headers specify GPL-3.0-only.

`%check` retains all three non-coverage targets used by upstream CI: C
white-box tests, design-by-design sunny-day tests, and the complete 378-case
black-box suite. The target repositories do not supply `cmocka-devel`, so
official SHA-256-pinned cmocka 1.1.8 is built as a test-only dependency; its
files do not enter the binary RPM. Installed smoke checks the version, installed design
configuration, and a create/remove roundtrip. These tests do not by
themselves prove native RISC-V hardware behavior or repository publication.
The repository's Apache-2.0 license covers original packaging files only.
