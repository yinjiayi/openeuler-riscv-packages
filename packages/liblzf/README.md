<!-- SPDX-License-Identifier: Apache-2.0 -->
# LibLZF

This directory packages the official LibLZF 3.6 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The official HTTPS archive is pinned by
SHA-256. Its members have one `liblzf-3.6` root and no unsafe paths.

The upstream Makefile has no test target. `%check` performs an actual CLI
compress/decompress round trip, and the installed smoke test exercises both
the public C API and CLI. The shared library retains the conventional
`liblzf.so.1` SONAME. The source's `LICENSE` permits BSD-2-Clause use; the
Apache-2.0 header covers only this repository's original packaging files.

The discovery snapshot corroborates LibLZF in Arch, Debian, Fedora, and
Ubuntu. No external distribution build recipe is executed. QEMU-user CI can
verify the functional round trips but cannot establish native RISC-V
performance. A passing PR build is not evidence of RPM repository publication.
