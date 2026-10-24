<!-- SPDX-License-Identifier: Apache-2.0 -->
# vtm

This directory packages upstream `https://github.com/directvt/vtm` version `2026.07.30` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The 240-minute package budget covers the large single-translation-unit C++ build under qemu-user while preserving upstream CTest discovery. Because upstream currently registers no CTest cases, both `%check` and the installed-RPM smoke test also execute `vtm --version` and require the packaged version.

Release 3 runs both version assertions inside a pseudo-terminal, a terminal
interface provided here by util-linux `script`. Upstream routes version text
through its terminal logger and suppresses that output when stdin is not a
terminal; CI run `34119156883` therefore captured an empty string and failed
the version assertion after compilation. `script --return` preserves the
child exit status, and the version comparison remains mandatory. The fixed
CI image includes util-linux for the installed smoke test; the SPEC also
declares it as a build requirement. The CTest invocation, binary features,
debug information, and build budget are unchanged.
