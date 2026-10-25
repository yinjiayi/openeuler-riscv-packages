<!-- SPDX-License-Identifier: Apache-2.0 -->
# libshine

This directory packages the official Shine 3.1.1 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The HTTPS release tarball is pinned by
SHA-256 and was inspected for unsafe archive paths. Its `COPYING` file
contains GNU Library GPL version 2; generated Autotools helper programs
are build inputs, not installed runtime components.

Shine supplies a fixed-point MP3 encoder library and `shineenc` CLI.
The single downstream patch makes its pkg-config file honor the configured
`lib64` directory; it does not alter encoder code.
The release does not register native Automake tests. The package keeps
`make check` and adds a functional encode check using the upstream WAV
fixture, plus an installed C API and CLI encode smoke. JavaScript tests
in `js/test` target Emscripten/Node/browser code rather than the native
C library, so they are not claimed as RISC-V validation. The native checks
prove frame production and API linkage, not encoded audio fidelity.

No external distribution recipe or AUR script is executed. CI must
establish the target build, functional check, and installed smoke result;
no target success or repository publication is asserted beforehand.
