<!-- SPDX-License-Identifier: Apache-2.0 -->
# pick

This directory packages upstream `https://github.com/mptre/pick` version `4.0.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Official `v4.0.0` resolves to commit `7a759de8f50cd03dd43de4af7e807fab4d2a7091`.
The official fixed archive SHA-256 is
`c62b1372b8c21d64c6da5a687abf3b56ee314fae5b67c1f08b5550ea5f87fdac`.
MIT covers the application; bundled reallocarray and strtonum retain ISC notices
verbatim in both binary packages. Linux's original pledge compatibility stub
is preserved and is not advertised as sandboxing.

Default configure/build and unfiltered `make test` remain enabled. All 31
original `.t` files, original PTY driver and its two-second timeout are unchanged.
The tests subpackage carries a pristine patched source archive; staged and
installed replay configure and compile only that original driver, then execute
its default suite against the packaged executable. `glibc-all-langpacks` supplies
en_US.UTF-8; `ncurses-base` supplies xterm terminfo.

Patch 1 bounds incomplete CSI/OSC escape-sequence lengths at the terminator.
Eight extra functional cases cover empty/plain, lone escape, truncated CSI/OSC
and complete CSI/OSC strings. Patch 2 ships those checks and installed replay
through supported SRPM patch staging; package-local test files and patched
source copies must be byte-identical. Remove patch 1 when an official fixed
release passes the same regression; remove patch 2 when upstream supplies
equivalent installed-default-suite replay. Neither was submitted upstream.

Fixed target: openEuler 24.03 LTS SP3 riscv64/RVA23, locked QEMU-user image.
PTY tests are functional evidence only, not native job-control, signal timing,
privileged-terminal, performance or memory-safety validation. No local compiler,
upstream script, RPM or QEMU build was executed. Build/install acceptance awaits
exact-head hosted CI and physical RPM/SRPM verification; a PR is not acceptance.
