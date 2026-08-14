<!-- SPDX-License-Identifier: Apache-2.0 -->
# clzip

This directory packages upstream `clzip` version `1.16` for openEuler 24.03
LTS SP3 on `riscv64`/RVA23.

The immutable discovery snapshot
`discovery-20260808T165000Z-9a89920c269462cd` identifies Debian stable
`1.15-3` and openSUSE Tumbleweed `1.16-1.4` as distribution lineage. The
snapshot's separate Ubuntu `1.16~rc2-3` record is pre-release rejection
evidence and is not used as stable source evidence. No distribution recipe
was read or executed.

The publisher's HTTPS index records final version `1.16` on 2026-03-15. Its
archive is pinned by SHA-256 and contains 38 regular files below the single
`clzip-1.16` top-level directory, with no links, special files, absolute paths,
or parent-directory traversal. A detached signature is published alongside
the archive, but it is not claimed as verified because a trusted full signer
fingerprint was not established. The committed SHA-256 remains mandatory.

The complete upstream test gate is `make check`. Its maintained test script
covers compression and decompression, concatenated and multi-member streams,
listing, stdin/stdout and file handling, invalid options, malformed headers,
truncated streams, trailing data, and corruption detection. CI may access the
network during the target build, while every fetched source remains bound to
its committed digest.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
