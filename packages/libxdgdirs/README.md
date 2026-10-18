<!-- SPDX-License-Identifier: Apache-2.0 -->
# libxdgdirs

This directory packages upstream `https://github.com/Jorenar/libXDGdirs` version `1.1.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The build selects the verified case-sensitive `libXDGdirs-1.1.3` archive root and uses an out-of-source release configuration. A minimal CMake patch makes the upstream test follow the standard `BUILD_TESTING` option, so CI runs it without changing the packaged library to a Debug build. A second test-only patch exports the fixture's `XDG_DATA_HOME` value so the child process under test observes it. Release 4 disables the inapplicable automatic debuginfo subpackage because the installed payload is a static library and header with no debuggable ELF file; the upstream CTest remains enabled.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
