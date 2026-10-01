<!-- SPDX-License-Identifier: Apache-2.0 -->
# libhtp

This package maps the frozen inventory's exact `libhtp` key to the
[official OISF stable 0.5.53 release](https://github.com/OISF/libhtp/releases/tag/0.5.53)
for openEuler 24.03 LTS SP3 `riscv64`/RVA23. The annotated release tag
resolves to immutable commit `16e23594c61f7719f8cb1cd19ca69bbafb37a0eb`.
The independently downloaded commit archive has SHA-256
`47413d7da92edf6becec880985e660f2ece95c755ab59becfd062d369c71e35f`;
CI fetches that URL and verifies the digest. Archive entries remain under its
top-level directory and contain no path traversal or symlink escapes.

The upstream `make check` compiles its `test_all` and `test_fuzz` programs and
runs the full registered `test_all` HTTP parser suite against bundled fixtures.
The standalone fuzz harness is compiled but not run without a bounded corpus;
this is upstream's default test contract, not a skipped registered test. The
registered suite includes a 2,000-transaction stress case. Installed-RPM smoke
compiles a client against the public header and library, creates/destroys a
configuration, and checks the reported version. Only target CI, not local x86
compilation, can establish RISC-V build, test, and installation results.

The first exact-head CI build succeeded, but installed smoke failed because
`htp_decompressors.h` publicly includes `<zlib.h>` and `libhtp-devel` did not
require `zlib-devel`. The devel package now declares that runtime development
dependency; the full upstream check and installed smoke remain unchanged.

Upstream library code is BSD-3-Clause. Its embedded LZMA decoder declares
public domain; the vendored BSD-3-Clause Google Test code is compiled for
upstream tests only and is not installed. CI artifacts do not by themselves
establish publication in the public RPM repository.
