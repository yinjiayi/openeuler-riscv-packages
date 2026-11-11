<!-- SPDX-License-Identifier: Apache-2.0 -->
# PicoSHA2

PicoSHA2 1.0.1 from official commit `161cb3fc4170fa7a3eca9e582cebd27cc4d1fe29`,
complete nine-file archive SHA-256
`6cf473a00c98298d3ddee0aed853e3c799791f49dbc01c996ea46cb248e85802`.
The upstream MIT grant and copyright are retained. Discovery is Debian wabt's
bundled component, not a claim of a standalone Debian package or version match.

This package installs the unchanged public header and original `test/test.cpp`.
Target builds enable the original registered CTest and both examples. The complete
suite exercises 20 checks for each of 10 known samples and two file-stream checks:
202 checks, without case filters or source patches. Because upstream prints a
failed check but still returns zero, the packaging oracle additionally requires
exactly 202 success lines and rejects failure lines. `test.cpp` is kept unchanged
and nonempty in the working directory expected by its file-stream tests.
Staged and installed verification recompiles that same test against the actual
public header, not a bundled replacement implementation. Assertions stay enabled.

Repository tooling and checksum verification are not RISC-V build evidence.
Exact-head CI, ordinary installation and physical RPM/SRPM review must pass before
merge. No local RPM/QEMU build, performance measurement or cryptographic security
assurance is claimed. Third-party source retains its own license; repository
licensing covers only original packaging material.
