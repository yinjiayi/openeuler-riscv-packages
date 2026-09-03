<!-- SPDX-License-Identifier: Apache-2.0 -->
# unifdef

This directory packages upstream `unifdef` version `2.12` for openEuler
24.03 LTS SP3 on `riscv64`/RVA23.

The frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd`
cross-checks Arch Extra `2.12-4`, Fedora 44 `2.12-7.fc44`, Debian stable
`2.12-1`, Ubuntu `2.12-1`, and openSUSE Tumbleweed `2.12-3.5`. These are
exact `unifdef` lineage rows; no external packaging recipe was read as
executable content or executed.

The upstream project page identifies `2.12` as the current release and links
the official XZ archive. Its exact bytes are pinned at SHA-256
`43ce0f02ecdcdc723b2475575563ddb192e988c886d368260bc0a63aee3ac400`.
The archive has one top-level directory and no unsafe paths, links, or special
files. It contains the complete shell-driven regression corpus, including
argument handling, expression evaluation, malformed input, exit modes,
recursive definitions, whitespace, line directives, and `unifdefall` cases.
`%check` runs upstream `make test` unchanged and offline.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
