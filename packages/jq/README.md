<!-- SPDX-License-Identifier: Apache-2.0 -->
# jq

This directory packages jq `1.8.2` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official GitHub release asset is pinned by SHA-256; the
published asset digest matches the independently downloaded bytes and the
archive passed safety inspection. Arch stable and openSUSE Tumbleweed confirm
1.8.2, while Fedora 44, Debian stable, and Ubuntu 26.04 LTS GA retained older
stable lines. This is therefore an intentional official-stable forward release.

AUR was queried through RPC only. The matching row is a VCS package and was
not used as source evidence; no PKGBUILD or distribution spec was executed.
The build requires the fixed target's system Oniguruma and fails closed if jq
tries to configure its bundled copy. Valgrind is disabled rather than used
under QEMU, but the complete upstream `make check` suite still runs. The
installed smoke test exercises the CLI and public libjq API without network.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
