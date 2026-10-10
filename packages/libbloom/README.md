<!-- SPDX-License-Identifier: Apache-2.0 -->
# Libbloom

This directory packages the official libbloom 2.0 tag for openEuler 24.03
LTS SP3 on `riscv64`/RVA23. The upstream tag resolves to commit
`57b35ea256b803b5fa6cd7cd2a2c36ecff9109c9`. Its HTTPS source archive
has SHA-256 `59965451ef033b0e060c9d7e472ead06af1ac61beddde11fe3ed4f5f4587bda6`.
All archive members remain under the `libbloom-2.0/` directory; no archive
member has an absolute path, parent traversal, or special-file type.

The frozen inventory marked this component `license-blocked`. Inspection of
the official source resolves the flag: the main library's `LICENSE` is
BSD-2-Clause, while `murmur2/README` says the bundled MurmurHash2 code is
public-domain and offers MIT terms for business use. The RPM license
expression selects the MIT grant for that bundled code. Both notices are
installed as license files. Apache-2.0 covers only these packaging files.

`%check` runs upstream's complete default `make test` target, exercising the
shared and static libraries. Upstream's optional `release_test` adds valgrind,
graphing and a large collision workload; `collision_test` warns that it can
take days on a slow machine. Neither optional benchmark is claimed as test
evidence. Installed smoke compiles and links a consumer, verifies a filter
miss, insert, hit and reset. Performance and long-running release testing
remain `needs-native-RISC-V`; passing QEMU-user CI is not repository
publication evidence.
