# nq 1.0

Canonical component: `github.com-leahneukirchen-nq`. Official `v1.0` points to
`2bb551efd8b3e50d715482a8f3b89f88bae74397`. Discovery lineage is `aur:nq` in
`discovery-20260808T165000Z-9a89920c269462cd`; the stale AUR observation was
rechecked against official tags, not executed as packaging instructions.

Fixed official source: <https://codeload.github.com/leahneukirchen/nq/tar.gz/2bb551efd8b3e50d715482a8f3b89f88bae74397>.
SHA-256: `58dcec1ffda79272c87984f9727e748f3d7758030a7b7c9c8440fc4006bd3fb2`.
No detached upstream signature is provided. COPYING, C headers and manuals
dedicate this work under CC0-1.0. All original notices and 15 archive members are
retained; no source patch is applied.

The recipe preserves default `make all`, all three installed commands/manuals,
`-Wall -O2`, and exact original `make check` / 36-case TAP suite. Only normal RPM
prefix, compiler/hardening flags and DESTDIR are supplied. Additional staged and
installed checks repeat the unchanged original suite, check archive/notices and
CLI behavior, and exercise nqterm without a terminal multiplexer. tmux and screen
are recommended for original interactive modes; no interactive session is claimed
as tested. Optional shell alternatives and zsh completion remain in the original
archive, as upstream's default install does not install them.

Build/check dependencies: gcc, glibc-devel, make, tar, gzip, coreutils,
perl-Test-Harness (`prove`), python3, grep, sed, bash. Complete target
primary/filelists admission is not DNF solver or physical RPM acceptance.
The official filesystem GHOST at `/usr/lib/debug/usr/bin` must be resolved with
this candidate's actual RPM modes and ordinary installation before merge;
no generic GHOST waiver applies.

Target is only locked openEuler 24.03 LTS SP3 riscv64/RVA23. Local work runs
repository validation, golden tests and source verification only. CI must prove
real build/install, unchanged original tests and RPM/SRPM bytes at exact head.
Userspace results do not prove native kernel scheduling, timing, performance,
multi-user security or interactive terminal behavior. If QEMU cannot support a
test, preserve and classify its failure; do not skip or weaken it.
