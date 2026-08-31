<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmodbus

This directory packages libmodbus `3.2.0` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official `v3.2.0` tag resolves to immutable commit
`a9b025d12289855490b10d77461c99e001abfc0f`; its SHA-256-pinned archive is
single-rooted and contains no unsafe paths, links, or special members. It
includes the upstream LGPL-2.1-or-later license and maintained test programs.

Frozen Arch metadata supplies component discovery lineage. It was used only as
read-only catalog evidence; no distribution recipe was read or executed. A
full target metadata and alias scan found no libmodbus package, provider, or
consumer, and libtool version-info `6:0:1` produces `libmodbus.so.5`. The target
primary repository contains the complete build/test dependency closure.

`%check` runs the registered upstream client/server unit suite and the separate
maintained TCP proxy integration suite. Both use bounded loopback servers on
non-privileged ports, require no external network, and preserve the upstream
test logic. Installed smoke verifies the SONAME and compiles a public API test
that creates and frees a TCP context without opening a connection.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
