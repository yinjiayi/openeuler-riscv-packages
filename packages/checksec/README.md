<!-- SPDX-License-Identifier: Apache-2.0 -->
# checksec

This directory packages upstream `checksec` 3.2.0 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The official tag archive is pinned independently by SHA-256. Version 3.2.0 is the Go implementation; the archive's `checksec.bash` file identifies itself as the historical, unmaintained 2.7.1 implementation and is deliberately not installed. The package requests the exact Go 1.25.0 toolchain, builds the pure-Go executable without an external-link PIE mode, resolves the upstream module graph with `-mod=readonly`, and relies on upstream `go.sum` hashes to authenticate downloaded modules. Package metadata therefore declares that the build uses network access. The target release's RPM `debugedit` cannot consume Go 1.25 DWARF and produces an empty debugsource manifest, so the unusable debug subpackage is explicitly disabled, consistent with other pure-Go packages in this repository.

`%check` runs the complete upstream Go test graph and exercises the built CLI against `/usr/bin/bash` with structured JSON output. Installed smoke repeats the version and ELF-file checks. These checks validate the userspace CLI under the RVA23 QEMU environment; they do not claim native execution or target-kernel inspection.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
