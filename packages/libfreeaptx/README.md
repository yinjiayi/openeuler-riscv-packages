<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfreeaptx

This directory packages libfreeaptx 0.2.2 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official 0.2.2 tag resolves to immutable commit
`6dee419f934ec781e531f885f7e8e740752e67d1`. Its archive is SHA-256
pinned and can be fetched over HTTPS in the target build. Upstream source
headers specify LGPL-2.1-or-later, matching the bundled `COPYING` license.

Upstream has no automated test target. `%check` runs standard aptX and aptX HD
encoder/decoder roundtrips on deterministic 24-bit stereo PCM and checks that
the decoded byte counts equal the input byte count. Installed smoke repeats
both modes and compiles a client against the public header through
`pkg-config`. The codec is lossy: byte-count checks are not an audio fidelity
or cryptographic claim. No audio hardware, network service, or privilege is
required.

The repository's Apache-2.0 license covers original packaging files only.
Passing CI does not establish repository publication or native RISC-V proof.
