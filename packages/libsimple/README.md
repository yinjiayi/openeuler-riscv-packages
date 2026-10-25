<!-- SPDX-License-Identifier: MIT -->
# libsimple 1.8

This packages Mattias Andrée's C utility library for openEuler 24.03 LTS SP3,
`riscv64`/RVA23. It is not an unrelated package with a similar "simple" name.

## Source and rights

The frozen discovery row is AUR `libsimple` 1.8-1 from snapshot
`discovery-20260808T165000Z-9a89920c269462cd`; it is lineage, not executable
packaging or proof of upstream acceptance. The official tag is
[`1.8`](https://codeberg.org/maandree/libsimple/releases/tag/1.8), whose signed
message is "Version 1.8". The archive is
[`1.8.tar.gz`](https://codeberg.org/maandree/libsimple/archive/1.8.tar.gz),
SHA-256 `ba2d966a57306ebde428d53e4808476ddf59113943b19e304d9e70baa266363d`.
It has the fixed `libsimple` root, 1353 ordinary members and 625 internal
symlinks. Every ordinary byte and symlink target was independently matched to
the exact Git tree. No source member is executed during local intake.

Annotated tag `e4cff137306ff1b9f161da369fccd89eec91a619` and commit
`b1d1158db0b9634a59dc717a7f0622e1da3df6f4` were independently verified using
the maintainer's official-profile-linked public key, fingerprint
`3683C4B70CFA859F0173F2CCE0DD13EBFC7D5E3E`. Both signatures were valid and
the certificate current at verification. There is no separate detached archive
signature: `sources.yaml` therefore does not invent one. Archive SHA-256 and
complete Git-member binding complement, rather than replace, that verification.

The full root ISC grant names Mattias Andrée (2017, 2018, 2021–2025).
1127 ordinary members explicitly refer to it; 217 project manual sources and
eight top-level/build files fall under its software-wide grant, plus the
LICENSE itself. No foreign grant, binary fixture or generated web asset was
observed. All 1353 original ordinary files are copied unchanged to `.notice`
files before adding package-local code; both build checks and installed smoke
validate the complete SHA-256 manifest. Internal symlink targets and all manual
aliases are preserved separately by normal installation.

## Original defaults and package adaptation

The original `make all` builds both static and shared libraries and all 1074
original test programs. The original fail-fast `make check` is retained without
`CHECK_PREFIX`, source deletion or feature switches. Its target count is not an
assertion count: 741 source files have literal no-op mains and 56 contain TODO
test markers (overlapping static inventories). The package exposes full output
and rejects upstream warnings about missing allocator interception or the
conditional `vasprintfa` test. Nothing here claims coverage of the untested
kernel-facing helpers, native timing, privileged behavior or security properties.

C11, all four original feature macros, warnings, test `-O0` overrides and libm
are retained. RPM optimization/link-hardening flags are used and `-UNDEBUG`
keeps package-local assertions active; RPM, not upstream `-s`, handles stripping.
There is no configure/bootstrap, generated documentation or external test data.
Normal upstream installation installs all 50 public headers and all 842 committed
manual files/aliases. Since it hardcodes `/usr/lib` rather than exposing LIBDIR,
the recipe moves its complete four-entry library set to `/usr/lib64`, preserving
the original `.so`/`.so.1` relative link chain and static archive. No pkg-config
interface is invented.

Six additional deterministic API cases cover binary duplication/ownership,
integer end pointers and overflow, case-sensitive prefixes, bounded comparison
with embedded NUL, binary subsequence search, and decimal timespec conversion
including its error path. Volatile function pointers require six actual external
library calls, not inline substitutes. Installed smoke runs the absolute installed
driver with inherited loader overrides removed, retains raw loader trace, its
hash and real failure status, and requires all six exact normal-symbol bindings
from that driver to the same installed shared file using `-ef`. It does not
assume that the loader spells a path `/usr/lib64` rather than an equivalent alias.

## Evidence boundary

The first exact-head target run (40184744585, attempt 1) exhausted the original
60-minute job budget during the default build, after 3235 seconds of rpmbuild.
It had not reached installation or `make check`; there was no observed fatal
compiler error. The package budget is now a bounded 180 minutes, as supported
by the existing workflow, to allow the complete unchanged workload to finish.
The SPEC, parallelism, flags, 1074 original test targets and six added API cases
are unchanged. This is a budget repair, not a source fix or proof that the
replacement run will pass; its fresh complete build/install results are required.

The recipe needs no undeclared network fetch. This does not claim network
isolation by the actual CI bridge. Local checks are trusted repository tooling,
schema, syntax and checksum/source-materialization checks only: upstream source,
compiler, RPM and QEMU execution are deliberately not performed locally.
Official complete primary/filelists metadata support dependency/path projection;
that is not a DNF SAT-solver result or acceptance of supplemental repositories.
Exact-head target build/install, all original invocations, six API/binding cases,
physical RPM/SRPM notices/payload and the complete enabled repository namespace
remain mandatory before merge. Automatic merge is not enabled.
