<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXau

This directory packages X.Org libXau 1.0.12 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official X.Org source archive is SHA-256 pinned. Target
builds may download it over HTTPS but must verify its bytes before `rpmbuild`.

`%check` retains upstream `make check` and checks that its `Autest` actually
writes a nonempty authorization file. Upstream `Autest` contains a return
expression that always reports success, so the installed-package smoke also
compiles a public-API write/read roundtrip and compares its fields. This is
functional smoke, not native RISC-V or repository publication evidence.

The upstream COPYING license is MIT-style. The repository's Apache-2.0
license applies only to original packaging files.
