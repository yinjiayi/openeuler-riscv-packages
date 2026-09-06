<!-- SPDX-License-Identifier: Apache-2.0 -->
# wavpack

This directory packages WavPack `5.9.0` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Fedora 44 GA and Arch stable package the same release;
openSUSE Tumbleweed and Ubuntu GA corroborate it, while Debian stable remains
on the older `5.8.1` line.

The source is the official upstream asset for the latest stable GitHub
release. The independently calculated SHA-256
`b5291bc4e6d69ebbd3da3800c5bf4a70f19bb92679b23e09b3b612c1e648d1ff`
matches GitHub's publisher digest. Its CMake, library, CLI, public-header, and
test inputs used by this build are byte-identical to tag `5.9.0`, which
resolves to commit
`5803634a030e2a11dba602ba057b89cc34486c67`.
Archive inspection found one expected root, no absolute or parent-traversal
path, no link, and no special entry. Built and installed code is BSD-3-Clause
plus the explicitly public-domain CLI MD5 implementation. The source asset
also carries BSD-2-Clause Windows-only support and generated Autotools helpers
with embedded GPL, FSF-permissive, X11, and exception notices; the riscv64
CMake build does not compile or install those platform/tooling files. AUR RPC
returned the cross-compilation variant `android-riscv64-wavpack`; no AUR
recipe or distribution build script was read or executed.

The fixed openEuler 24.03 LTS SP3 RVA23 repository contains epoch-zero WavPack
`5.6.0-1.oe2403sp3` and the `libwavpack.so.1` ABI. This epoch-zero
`5.9.0-1` release base advances EVR without changing that SONAME; the
official 5.6.0 and 5.9.0 export manifests are also identical. Its build
requirements are available in the same fixed repository.
The network-free `%check` first runs upstream's registered short,
no-extras exhaustive CTest and then the complete `all-tests` equivalent with
twelve `wvtest` threads, without downstream skips. The installed smoke test
round-trips real PCM audio and links the public C API.

RISC-V status remains `unknown` until the pinned openEuler RVA23/QEMU CI
completes; successful source testing on another architecture is not target
evidence.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, and documentation.
