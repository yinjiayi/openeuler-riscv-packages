<!-- SPDX-License-Identifier: Apache-2.0 -->
# treefrog-framework

This directory packages upstream `https://github.com/treefrogframework/treefrog-framework` version `2.12.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Packaging release 2 uses TreeFrog's project-specific `configure` interface
with its supported installation-directory options. The preceding exact-head
RVA23 build showed that the generic RPM configure macro supplied unsupported
GNU triplet and dependency-tracking arguments, causing the script to print
usage without generating Makefiles. The build, upstream check target, and
install smoke test remain enabled.

Packaging release 3 adds the Qt 6 declarative development package required by
the framework's qmake project after the next exact-head RVA23 build reached
configuration and reported the QML module missing.

Packaging release 4 enables TreeFrog's supported shared MongoDB C driver mode
and declares `mongo-c-driver-devel`, which is present in the approved official
RVA23 repository. This retains MongoDB support while avoiding the bundled
driver build that failed in the following exact-head CI run. The upstream check
target and install smoke test remain enabled.

Packaging release 5 follows TreeFrog's documented two-project layout by
building and installing `src` and `tools` separately. This corrects the next
exact-head failure, where the configured source tree intentionally had no
top-level Makefile. The check phase now runs the upstream source and `tmake`
test suites with locally bound Redis and Memcached instances whose exact PIDs
are verified and cleaned up. The install smoke test remains enabled.

Packaging release 6 raises the QEMU build timeout from 60 to 180 minutes. The
preceding exact-head run exhausted its bounded 2800-second build-command budget
while `src` was still compiling normally, with no compiler or test failure.
The longer timeout preserves the complete build and test paths.
