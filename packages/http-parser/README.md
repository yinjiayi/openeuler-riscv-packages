<!-- SPDX-License-Identifier: Apache-2.0 -->
# http-parser

This directory packages http-parser 2.9.4 release 4 for openEuler 24.03 LTS
SP3 on `riscv64`/RVA23. Release 4 preserves the target repository's existing
2.9.4 EVR while replacing its recipe with the audited package-only manifest.
The source is the immutable archive for upstream's final stable `v2.9.4` tag
(commit `2343fd6b5214b2ded2cdcf76de2bf60903bb90cd`) and is pinned by a locally
calculated SHA-256 in `sources.yaml`.

Frozen discovery snapshot `discovery-20260812T010000Z-b30-http-parser`
records AUR `2.9.4-2`, Debian stable `2.9.4-6`, Fedora 44
`2.9.4-16.fc44`, openSUSE Tumbleweed `2.9.4-1.21`, and Ubuntu Resolute
`2.9.4-6build2`. Distribution metadata was used only as lineage evidence; no
distribution recipe was read or executed.

`%check` invokes upstream's complete `make test` target. It builds and runs
both the strict parser suite (`HTTP_PARSER_STRICT=1`) and the fast permissive
suite (`HTTP_PARSER_STRICT=0`); neither mode is omitted. The installed smoke
test compiles a consumer, parses a complete HTTP request through the shared
library, and checks the request method and completion callback.

http-parser is MIT. Apache-2.0 covers only this repository's original
packaging metadata and scripts.
