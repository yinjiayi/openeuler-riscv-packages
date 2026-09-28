<!-- SPDX-License-Identifier: Apache-2.0 -->
# libharu

This directory packages the official libHaru 2.4.6 stable release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The upstream
[`v2.4.6` release](https://github.com/libharu/libharu/releases/tag/v2.4.6)
resolves to commit `3467749fd1c0ab6ca6ed424d053b1ea53c1bf67c`. GitHub's
official HTTPS tag archive is pinned to SHA-256
`ec8f327520d1d354ce58b5d2af75b64f380cddc522437c169463b39760921348`.
The archive has 347 entries in one root, all regular files or directories,
with no unsafe paths or duplicate names.

The frozen inventory identifies `libharu` as a discovered, not-yet-managed
component. The live Arch Extra 2.4.6-1 package is an independent lineage
cross-check; its recipe was not executed. Upstream `LICENSE` is Zlib.

Upstream does not register a test suite. `%check` compiles and runs a small
program using the built RISC-V library, writes a PDF, and checks its header
and trailer. Installed-RPM smoke performs the same public C API operation
against the packaged library. Neither check implies that all PDF features
have been tested. The unbuilt language bindings are installed only as
upstream documentation.

External source remains under its upstream Zlib license. Apache-2.0 covers
only the original packaging metadata, script, and documentation here.
