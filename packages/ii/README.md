<!-- SPDX-License-Identifier: Apache-2.0 -->
# ii

This directory packages upstream `https://tools.suckless.org/ii/` version `2.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Official source: [ii 2.0](https://dl.suckless.org/tools/ii-2.0.tar.gz), SHA-256
`4f67afcd208c07939b88aadbf21497a702ad0a07f9b5a6ce861f9f39ffe5425b`.
The official stable page and all eight archive members were reviewed. Debian,
Fedora and Ubuntu discovery lineage is metadata only; no distribution recipe
was executed. Canonical identity is `tools.suckless.org-ii`, RPM name `ii`.

The package license is `MIT AND ISC`. Original `LICENSE` (MIT/X Consortium) and
`arg.h`'s "Copy me if you can. by 20h" notice remain intact. Bundled `strlcpy.c`
had only "Taken from OpenBSD"; its function was compared against official
[OpenBSD revision b9c631e7e9c23759a6745d2a0a470cc5cb8f7cc0](https://github.com/openbsd/src/blob/b9c631e7e9c23759a6745d2a0a470cc5cb8f7cc0/lib/libc/string/strlcpy.c)
(file SHA-256 `ed7466d19670c53b200e805fb0de8d6a7ff6033e05a047030bd56a7d13c3aec6`).
Every function token matches after removing comments/whitespace and normalizing
equivalent NUL literals. Patch `0001` restores Todd C. Miller's 1998 ISC copyright
and permission notice only; executable tokens, bundled fallback and all build
defaults are unchanged. Both binary subpackages install the MIT and ISC notices.
This downstream notice restoration is removable when stable upstream includes
that notice. No upstream write was made.

Original `make all` and `make install` are preserved, with system CFLAGS/LDFLAGS,
bundled `strlcpy.o`, VERSION and `_DEFAULT_SOURCE` defaults. Only standard RPM
prefix/man/doc/staging paths are supplied. Upstream declares no check/test target;
no default test is removed or filtered. The downstream Python fixtures are
mandatory both in `%check` against the staged binary and after ordinary RPM
installation via `ii-tests` and `tests/smoke.sh`.

An offline fixture is a private fake IRC endpoint using a temporary Unix socket
or numeric loopback TCP listener, not a public IRC service. It checks exact
PASS/NICK/USER registration, PING/PONG, 0700 FIFO/directory permissions, JOIN,
outgoing/incoming channel/private messages and logs, topic/away/nick/raw commands,
PART FIFO removal, QUIT and SIGTERM cleanup, plus CLI/socket/service errors.
All processes and temporary paths are bounded and cleaned. The original archive
and notices are retained in the test RPM for independently repeatable checks.

Build dependencies are gcc, glibc-devel, make, tar, gzip, coreutils and python3;
runtime libc is generated from ELF requirements. Tests additionally require
python3 and the exact main RPM. No network is used during build; the numeric
loopback/Unix fixtures never contact external IRC/DNS. Native kernel, timing,
performance, privileged or exhaustive IRC interoperability claims are outside
these tests. Upstream's optional external TLS tunnel is not a built-in feature
and is not claimed as tested. Exact-head target CI and physical RPM/SRPM/namespace
acceptance remain required; local validation does not establish target success.
