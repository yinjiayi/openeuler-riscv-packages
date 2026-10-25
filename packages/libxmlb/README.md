<!-- SPDX-License-Identifier: Apache-2.0 -->
# Libxmlb

This directory packages the official libxmlb 0.3.29 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The release's published SHA-256 is
`448294be33bfae62f00fa66e506f1cae80237ce71b7ab6530aefa75005eeb08a`,
and it matches the HTTPS tarball bytes. All archive members stay inside a
single top-level directory; none are absolute or parent-traversing. The
upstream library is LGPL-2.1-or-later; Apache-2.0 governs packaging files.

The build retains upstream's default CLI, GObject Introspection, gtk-doc,
lzma, zstd, and test features. Complete registered Meson tests run under QEMU
user mode. The installed smoke test uses `xb-tool` to compile and query a
small XML fixture and compiles a program using the installed pkg-config
metadata. Upstream installed tests and fixtures are packaged separately.

The frozen Arch record is discovery lineage only and is not an executed
packaging recipe. QEMU-user functional checks do not establish native RISC-V
timing or performance. A successful PR build does not establish publication.
