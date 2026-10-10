<!-- SPDX-License-Identifier: Apache-2.0 -->
# liblaxjson

This directory packages liblaxjson 1.0.5 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official annotated 1.0.5 tag dereferences to commit
`9f55366a50c31c3be33705a3ee21d52eb77cb4ab`; that archive is pinned by
SHA-256 and may be fetched over HTTPS in the target build.

The frozen discovery snapshot marked the component `license-blocked` because
Debian/Ubuntu package metadata did not expose a license value. That is not
evidence of a proprietary license: the official tag's `COPYING` and C source
headers explicitly grant MIT. No external distribution recipe was executed.

`%check` runs the sole upstream CTest covering primitive parsing. Installed
smoke links against the public C API and verifies callbacks for a small JSON
object. Upstream's CMake files install libraries under `lib/`; the SPEC moves
those exact installed libraries into openEuler's architecture libdir. Passing
CI does not prove repository publication or native RISC-V operation.

The repository's Apache-2.0 license covers original packaging files only.
