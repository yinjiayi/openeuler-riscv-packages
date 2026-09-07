<!-- SPDX-License-Identifier: Apache-2.0 -->
# shmux

This directory packages upstream `https://github.com/shmux/shmux` version `1.0.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 2 declares the ncurses and PCRE development dependencies used by the
upstream configure script. The package `%check` stage invokes upstream's real
`make test` target, which runs its bundled command, analyzer, exit-code, and
timer behavior tests locally without contacting remote hosts.

Release 3 keeps all seven upstream test groups enabled while setting the
test-only soft file-descriptor limit to 1024. Upstream closes every descriptor
up to `RLIMIT_NOFILE` for each child process; bounding that limit avoids a
QEMU-amplified close loop and still exceeds the suite's maximum requirement.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
