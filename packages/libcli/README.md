<!-- SPDX-License-Identifier: Apache-2.0 -->
# Libcli

This directory packages the official libcli V1.10.7 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The tag resolves to commit
`0f8d257612a5c62000a55fd00e79a35f813f0375` and the HTTPS source archive
has SHA-256 `179f78592f73492c22cc1b544b6f8cb0f6630a2f670430c118b8e084e6562e74`.
All archive members remain under `libcli-1.10.7/`, with no absolute path,
parent traversal or special-file type. Upstream's `COPYING` contains LGPL 2.1
terms; Apache-2.0 covers only these packaging files.

The default upstream make target builds both libraries and its `clitest`
example. There is no automated upstream test target: `%check` confirms that
the example was compiled but does not claim to have executed a test suite.
The target base image contains `libxcrypt-devel` 4.4.36; the supplemental
repository's 4.5.2 candidate conflicts with the base `glibc-devel` and
`libxcrypt-static` pair, so BuildRequires caps the development dependency
below 4.5 until the repository versions are reconciled.
Installed smoke compiles and links a consumer, registers a command and checks
that dispatch invokes its callback with the expected argument. Network
sessions, interactive terminal behavior and native RISC-V performance remain
outside this QEMU-user smoke. Passing CI does not establish RPM repository
publication. Fedora data is discovery lineage only, not an executed recipe.
