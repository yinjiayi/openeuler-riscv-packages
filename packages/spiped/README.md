<!-- SPDX-License-Identifier: Apache-2.0 -->
# spiped

This directory packages [spiped](https://www.tarsnap.com/spiped.html) 1.6.4
for openEuler 24.03 LTS SP3, `riscv64`/RVA23. Spiped supplies authenticated
encrypted pipes between socket addresses; both `spiped` and `spipe` are included.

## Source and license

The official stable release, dated 2025-04-02, is
`https://www.tarsnap.com/spiped/spiped-1.6.4.tgz` (158,844 bytes). Its SHA-256 is
`424fb4d3769d912b04de43d21cc32748cdfd3121c4f1d26d549992a54678e06a`, matching
the publisher's HTTPS release page. Source acquisition checked all 213 regular
archive members for safe paths without executing them. The official GitHub tag
`1.6.4` is a lightweight tag at commit
`36e7f414b2eafbe274dd2838b6b2bd090d2977b1`, not a signed annotated tag.

The upstream README describes signed official releases, but the current official
spiped page links neither a detached signature nor a signed checksum manifest.
The exact `.tgz.asc`, `.tgz.sig` and `spiped-sigs-1.6.4.asc` URLs returned HTTP
404; the official GitHub releases list was empty. This is checksum-bound official
source verification, not a claimed signature verification. A newly published
signature must be independently verified before adopting its identity.

`COPYRIGHT` grants BSD-2-Clause for the project and refers to per-file terms for
external code. The sole bundled external file,
`libcperciva/external/queue/queue.h`, carries BSD-3-Clause. Both full notices are
installed by `%license`; neither is replaced with a shortened SPDX label.
The repository's Apache-2.0 license applies only to original packaging material.
No downstream recipe or patch is borrowed, and `patches/series` is empty.

Frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd` recorded
Arch extra 1.6.4-2, Debian stable/main 1.6.3-1 and Ubuntu resolute/universe
1.6.4-1. Their aliases are coalesced into this official component; those old
records are discovery lineage, not current source or target-build evidence.
The current managed directory and all open-PR exact-file census had no spiped
or spipe collision at intake. Refresh that census before remote submission.

## Recipe and dependencies

The shipped generated POSIX Makefiles are built with GNU make, GCC, RPM compiler
and linker flags, and OpenSSL `libcrypto`. `make all` is retained in full:
both programs, all libraries, seven functional helpers and three performance
helper binaries are compiled. Developer-only `Makefiles`/`publish` targets
require BSD make, but this release build does not invoke them. Architecture
probes and their portable C fallbacks remain unmodified. The install stage
copies the same two programs and manual pages as upstream without upstream's
early stripping, so RPM owns debug processing; it additionally retains QA.

Build requirements are bash, binutils, coreutils, diffutils, gcc, glibc-devel,
grep, make, openssl-devel, procps-ng and sed. Runtime QA uses bash, coreutils,
diffutils, grep, procps-ng and sed; automatic ELF requirements cover libc and
libcrypto. The official base repository's complete primary/filelists pair was
joined by full package identity: all declared requirements, command paths,
unconditional headers and runtime library providers closed over 94 packages,
with no material namespace or file ownership collision. Supplemental repository
namespace acceptance remains an independent merge gate, not a claimed result.
`/dev/urandom` is a required target device, not an RPM-owned file provider.

## Original checks and installed smoke

`%check` runs the unmodified default `make test`, without a scenario selector,
test patch or failure suppression. The ten original scenarios exercise:

1. TCP and UNIX-socket connection open/close;
2. connection timeout;
3. concurrent connections;
4. spipe file transfer and invalid-target exit;
5. spiped pair file transfer;
6. system-spiped interoperability (the original source-build conditional skip
   when no suitable system spiped exists remains visible);
7. local name/address resolution;
8. rate-limited full-duplex EOF/file equality;
9. all five pushbits modes and copy equality;
10. pthread blocking/thread-relative ordering.

The default suite uses only local loopback ports 8001-8003 and UNIX sockets.
Remote DNS and valgrind are upstream opt-ins, not enabled by the default target;
this recipe does not replace them with passing stubs. Test 10 checks relative
thread ordering, not a throughput or latency benchmark. Native hardware,
kernel-specific timing/performance and security assurance are not inferred from
QEMU functional results. A timing/emulation failure must be classified using
actual logs and may require native RISC-V; no test may be removed to get green.

Installed smoke verifies all 14 original shell-file SHA-256s and seven compiled
helper paths, then runs the unchanged original driver from a fresh short
temporary directory. Driver-relative links point to the RPM-installed binaries.
All ten scenarios must report success in smoke, including the unchanged system
interoperability check against `/usr/bin/spiped`; skipped scenarios are not
counted as installed smoke success. The 1,800-second outer deadline reports
failure rather than converting a hang into success. CI must keep the complete
build/check and installation/smoke logs for physical product acceptance.

No source configure, build, QA, RPM, installed smoke or QEMU was executed locally.
Metadata/unit/golden validation and offline verify-only source checks do not
establish RISC-V buildability. Current target state is `unknown`; hosted CI must
prove the real build, default checks, installation and smoke in the locked target
before merge consideration. Auto-merge is not enabled by this recipe.
