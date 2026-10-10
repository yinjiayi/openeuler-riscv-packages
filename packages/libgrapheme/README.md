<!-- SPDX-License-Identifier: Apache-2.0 -->
# libgrapheme

This package maps the frozen inventory's exact `libgrapheme` key to the
[official stable 3.0.0 release](https://libs.suckless.org/libgrapheme/) for
openEuler 24.03 LTS SP3 `riscv64`/RVA23. The release archive's SHA-256
`32585af73dda62fbcc0fed14f199aa1bc988ad01dad0bfbd06cf175d9cf3d68c`
matches both the [official sums](https://dl.suckless.org/libgrapheme/sha256sums.txt)
and independently downloaded bytes. All 102 archive members are regular
files or directories under the top-level release directory, with no path
traversal, symlinks, or device files. CI pins and verifies the digest.

The upstream `make test` target executes eight test programs, including
generated conformance cases from bundled Unicode 17 data. `%check` builds
and runs the same eight programs without exclusions, with explicit fail-fast
behavior because upstream's shell loop could mask an earlier failure. The
separate performance `benchmark` target is not part of the upstream default
tests. Installed-RPM smoke links a new
program against the public header/library and checks UTF-8 grapheme-break and
decode calls. Target CI, not a local x86 build, must establish the result.

Upstream code is ISC-licensed. The bundled Unicode data has the Unicode
License v3 (`Unicode-3.0`); both license texts are retained in the RPM.
CI build artifacts alone do not establish public RPM repository publication.
