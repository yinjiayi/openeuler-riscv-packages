<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfontenc

This directory packages the official X.Org libfontenc 1.1.9 release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The archive is SHA-256 pinned;
target builds may fetch it over HTTPS but must verify the bytes first.

Upstream registers no automated test programs, so `%make_build check` is not
counted as test coverage. `%check` additionally compiles and runs a public-API
test of the built-in ISO-8859-1 mapping. The installation smoke repeats that
check against installed runtime/development RPMs. Neither is native RISC-V
hardware evidence or proof of repository publication.

The core upstream source is MIT; `src/reallocarray.c`, a bundled compatibility
fallback, is ISC. The repository's Apache-2.0 license applies only to original
packaging files.
