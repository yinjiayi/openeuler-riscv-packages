<!-- SPDX-License-Identifier: Apache-2.0 -->
# utf8cpp

This directory packages upstream `https://github.com/nemtrif/utfcpp` version
`4.1.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch stable
`extra` (`utf8cpp` `4.1.1-1`), the AUR metadata-only `utf8cpp-git` entry
(`4.0.6.r7.gda71cf9-1`), Fedora 44 (`utf8cpp` `4.0.9-2.fc44`), openSUSE
Tumbleweed (`utfcpp` `4.0.8-1.4`), Debian stable (`utfcpp` `4.0.5-1`), and
Ubuntu Resolute GA (`utfcpp` `4.0.9-1`). These names resolve to the same
official upstream component. No AUR recipe or distribution build script was
read or executed.

The full upstream test gate means all six shipped CTest programs run: invalid
UTF-8 inputs, C++11, C++17, C++20, public API behavior, and the no-exceptions
configuration. The library is header-only and has no architecture-specific
code. Upstream tag `v4.1.1` still writes `4.1.0` into generated CMake version
metadata, so the install step verifies that exact known value before correcting
only the generated package-version file to `4.1.1`.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
