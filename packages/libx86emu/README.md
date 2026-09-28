<!-- SPDX-License-Identifier: Apache-2.0 -->
# libx86emu

This package maps the frozen inventory's exact `libx86emu` key to the
official [upstream 3.7 tag](https://github.com/wfeldt/libx86emu/tree/3.7)
for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The tag resolves to immutable
commit `ce81129c57fdfbf690bebc210a8db97d926cc5e7`; the corresponding
HTTPS source archive independently hashes to SHA-256
`832665403200c51c79fafac008357705251058a86784541a4b220ab05ac7283a`.
Its 133 members remain under one top-level directory without path traversal,
symlinks, or special files. CI verifies the pinned digest before building.

The official GitHub tag archive omits the generated `VERSION` file and Git
metadata required by `git2log`. `%prep` creates `VERSION` from the verified
tag and disables that Git-only changelog generator; no production source is
patched. The upstream `make test` target is retained in `%check`. It assembles
and executes all 60 x86 instruction fixtures using Nasm/ndisasm, compares 42
against upstream `.done` files, and treats the remaining 18 as run-only. The
target RVA23 repository lists `nasm` 2.16.01. Installed-RPM smoke compiles
against the public header and exercises the library lifecycle. CI artifacts
do not establish public RPM repository publication.

Upstream `LICENSE` and `LICENSE_INFO` permit redistribution under a
historical X11/HPND-style license; both are retained in the RPM.
