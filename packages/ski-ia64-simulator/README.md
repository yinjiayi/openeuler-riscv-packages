<!-- SPDX-License-Identifier: Apache-2.0 -->
# ski-ia64-simulator

This directory packages upstream `https://github.com/trofi/ski` version `1.5.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The upstream archive expands to `ski-1.5.1`. The SPEC names that source root explicitly and declares the code generators, pkg-config macros, libelf headers, and ncurses development files required by upstream `configure.ac`.

Exact-head CI run `33319503264` is bound to commit `ea43250d381c7ac6ba1984d5af87bc14ccfde94c`. Source verification passed for the official archive with SHA-256 `797e3443b605c861bd193e40e646ce687ee9679d0ecfe35758344d1456716f06`, then compilation failed in `src/linux/syscall-linux.c`. RISC-V follows the Linux asm-generic syscall table, which provides `getdents64` but not legacy `getdents` or `uselib`. The late inclusion of `sys/syscall.h` also replaced the simulator's HP-UX `SYS_lseek` value with the RISC-V host value `62`, colliding with the simulator's `SYS_FCNTL` case.

The downstream GPL-2.0-or-later patch keeps host calls in the `__NR_*` namespace and leaves the simulator's own HP-UX/IA-64 syscall numbers unchanged. When legacy `getdents` is absent, it reads the kernel's `linux_dirent64` layout, whose name begins after the 8-byte inode, 8-byte offset, 2-byte record length, and 1-byte type fields, then retains the existing conversion into guest IA-64 records. The host read is capped to the fixed local buffer. An unavailable `uselib`, or a host with neither directory syscall, returns `-1` with `errno=ENOSYS`, matching Linux's unsupported-system-call contract instead of pretending success.

All upstream tests remain enabled. This source-level and static validation is not a successful target build: RISC-V status remains `unknown` until the patched exact head completes build and smoke validation in the locked CI environment. In particular, the `getdents64` compatibility path relies on the Linux UAPI layout reviewed above; target CI remains authoritative for its runtime directory iteration behavior.

Exact-head CI run `33362442642` at commit `d8eef81a0a6b711060267a6d424b28eab9378b68` compiled the patched source and passed all upstream tests on the locked RVA23/QEMU environment. Packaging then failed because the generated file manifest captured uncompressed `.1` paths before openEuler's `brp-compress` renamed them. Release 4 excludes the manual-page tree from that generated manifest and owns it with `%{_mandir}/man1/*`, which matches the post-processing names without weakening the test suite. This remains a repair awaiting a fresh exact-head build and installed-RPM smoke result; it is not publication evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
