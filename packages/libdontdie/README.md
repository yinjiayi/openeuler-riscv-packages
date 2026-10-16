<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdontdie

Packages official `flonatel/libdontdie` stable 1.2.0 for openEuler 24.03
LTS SP3 riscv64/RVA23. This Linux `LD_PRELOAD` library intercepts `socket`
and enables TCP keepalive for newly created Internet stream sockets. It has
no public header/development API and no upstream install target; this RPM
preserves the upstream SONAME `libdontdie.so.0`, symlink layout and man page.

## Source and license

Official tag `1.2.0` resolves to
`3cc5c8a72599aed37efcb1343dbfb3630d7d3ce3`, tree
`f13a5f489fd9b143a81358a55be9549452096818`. Source SHA-256:
`5cd5d86d864efbc20bdb266259d1320fefd4306aad1351925d65ff9674338c5a`.
All 13 regular archive files match the authenticated Git blob inventory;
the fixed archive is not committed. No upstream signature is supplied;
HTTPS/Git identity/digest verification is not a signature claim.

The root MIT license (Andreas Florath) is installed unchanged. The original
Java example has a full Oracle/Andreas BSD-3-Clause notice, conditions and
disclaimer. Its entire unchanged source is also installed as `COPYING.Java`
in the binary license directory; original test sources remain with the
test applications and in the SRPM. `MIT AND BSD-3-Clause` describes these
upstream materials; new packaging/contract code is Apache-2.0 and does not
relicense upstream code. No distribution recipe or external source code is
executed locally, and no upstream write is made.

## Default build and dependencies

The unchanged `.travis.yml` builds `make all` and `make testapps`. Both
targets remain mandatory. All four original applications are built:
`test/Cblackbox/tcp_server`, `tcp_client`, `test/Cperformance/perf`, and
`test/java/EchoClient.class`. Environment CFLAGS/LDFLAGS retain the original
Makefile's additions, diagnostics and targets. No patch, skipped build
target, removed test or network-enabled build is introduced.

Complete official (18,503 records) and supplemental (1,244) primary and
filelists inventories supply the 15 BuildRequires roots, including
`java-17-openjdk-devel`. No package/library name or library path collision
was found. This metadata capability walk is not a DNF SAT or successful
installation claim; hosted CI must perform the actual dependency transaction.
Compiler/Java dependencies are retained for the installed test contract.

## Test definitions and evidence boundary

Upstream has no automated semantic test suite: `testapps` compiles manual
tools, not an assertion-based `make check`. Preserve those tools and their
sources rather than inventing an upstream pass count. A **bounded interface
check** means ping/EOF for each original C blackbox tool, one original
`perf` socket/close iteration without timing, and the original Java usage
error/status. These four checks do not exercise the manual connection or
packet-loss scenario.

A **downstream socket-option contract** is a fresh C consumer compiled
against system socket headers and run with the staged/installed library
via `LD_PRELOAD`. Its four modes are an unpreloaded disabled baseline,
preloaded default, explicitly disabled keepalive, and custom idle/interval/
probe values 7/3/4. Each checks Internet IPv4/IPv6 streams, untouched
datagram/Unix sockets, CLOEXEC/NONBLOCK preservation and invalid-family
error propagation. It uses `getsockopt`, not sleeps, packet loss, timers or
privileged firewall changes. Unsupported socket behavior is a failure,
not silently skipped or reported as a pass.

`%check` runs this contract against the staged install. Smoke verifies the
installed RPM with `rpm -V`, then replays the same contract and original
bounded interfaces; test source checksums, ELF SONAME and symlink are
mandatory. A failure is retained, not converted to success. The original
manual privileged keepalive/timing/performance scenarios require separately
authorized native Linux validation; this PR makes no such claim, no
thread-safety/security guarantee, and no full network/Java connection claim.

Local validation is limited to inert source review, source-only digest
verification, recipe checks, Bash syntax and trusted repository tooling
tests. Actual riscv64 compilation/install/functional results, physical
RPM/SRPM and CI acceptance are outstanding until exact-head hosted results
are independently verified. Submission is not a merge or public release;
Auto-merge remains off.
