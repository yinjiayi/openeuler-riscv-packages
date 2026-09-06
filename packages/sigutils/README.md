<!-- SPDX-License-Identifier: Apache-2.0 -->
# sigutils

This directory packages upstream `https://github.com/BatchDrake/sigutils` version `0.3.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The required build closure is expressed through the target repository's `pkgconfig(sndfile) >= 1.0.2` and `pkgconfig(fftw3f) >= 3.0` capabilities. CMake's Threads detection is satisfied by the declared CMake, GCC, and glibc development packages. Upstream treats VOLK as an optional acceleration path, and the fixed target repository does not provide `pkgconfig(volk)`, so this package does not require or claim VOLK support.

Upstream builds one `sutest` executable containing 18 test entries but does not register it with CTest. The RPM `%check` section therefore runs `sutest` directly so every entry is invoked. The real-capture entry retains upstream's own self-skip when its optional sample file, which is not present in the release archive, is unavailable.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
