<!-- SPDX-License-Identifier: Apache-2.0 -->
# libICE

This directory packages the official X.Org libICE 1.1.2 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The source is SHA-256 pinned and may be
retrieved over HTTPS in the target build only after digest verification.

Upstream registers no automated tests, so `make check` alone is not test
coverage. `%check` and the installed-package smoke each perform an ICE
authority record write/read roundtrip through the public API. The test uses
an anonymous temporary stream and requires no X server, network connection,
or privileged operation. XML specifications are installed; generated formats
are omitted to avoid optional documentation toolchain variability.

The upstream COPYING license is MIT. The repository's Apache-2.0 license
applies only to original packaging files. CI build success is not proof of
repository publication or native RISC-V validation.
