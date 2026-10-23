<!-- SPDX-License-Identifier: Apache-2.0 -->
# bchunk

This directory packages bchunk 1.2.2 for openEuler 24.03 LTS SP3,
riscv64/RVA23. The recipe itself is not a build, installation or publication result.
Official repository hessu/bchunk release/1.2.2 is annotated tag
`d52c36088c0ea01428120e9485cd73f77f934f7f`, peeled commit
`0c7009d1d2be1cc12edebf926010f417069b6211`, tree
`a02d4e06af6a564a366d993359ef4da88a35e82d`.
The commit-addressed 15,337-byte official archive has SHA-256
`3237587b7f258526dcb4258f6206057a2fb837a9bf7104a50fc307397033d2cc`.
Its seven regular files match the captured upstream Git tree. Tag/commit are
unsigned; no cryptographic signature verification is claimed. GPL-2.0-or-later
is stated by README and C source; COPYING is packaged unchanged.

Frozen discovery lineage identifies the same bchunk/he.fi component. The
working HTTPS source route is the author's GitHub repository, not the failed
legacy he.fi tarball. No distro recipe is executed or copied. The upstream
SPEC is stale (1.2.0) and is not used as the recipe.

The original Makefile default is `all: bchunk`; there is no test/check target or
bundled test suite in the complete fixed source tree. Source and all conversion
features remain unchanged. RPM compiler/linker flags are passed as Make
command-line variables, and the original all target builds the program. Manual
buildroot installation preserves both upstream products (binary and man page)
without the upstream install target's ownership changes or early stripping.
RPM's ordinary debug and man-page processing remain enabled. No source patch,
feature disable, test removal, privileged mount or optical drive is involved.

Packaging QA means new deterministic regression cases, not upstream test
passes. Identical embedded Python code in `%check` and `tests/smoke.sh` checks
15 conversions: MODE1/2352 (including verbose and CRLF), MODE2/2352
default/raw/PSX and raw precedence, MODE2/2336, audio CDR, swapped audio, WAV
and swapped WAV, unknown-mode fallback, and mixed/audio multitrack boundaries.
Six CLI/error cases check help, missing arguments, missing BIN, missing CUE,
empty CUE and malformed TRACK status. Exact output filenames, payload bytes,
all 44 WAV-header bytes and return codes are checked; no assertions are
disabled and no failure is ignored. The PSX expected bytes follow source
offset 0/size 2336, not the inconsistent offset 24 in help/man text.
Each execution uses a fresh automatically cleaned private directory and
bounded subprocesses. `%check` selects the built executable; installed smoke
queries the RPM and selects `/usr/bin/bchunk`, never a build-tree fallback.
Bash and Python 3 are explicit QA runtime dependencies rather than intrinsic
requirements of the C converter. They must be included in provider closure.

No local source/QA/RPM/QEMU execution is claimed. Admission requires current
canonical/open-PR identity checks, provider/owned-path closure and repository
validation. All declared source-level dependencies are available from the
official target base repository; the supplemental service is not selected as a
dependency source. Build-generated ELF build IDs, expanded doc/license paths,
actual RPM headers and installed behavior still require exact-head CI and
physical RPM/SRPM/install evidence. A file-only qemu-user profile is a scheduling
proposal, not an RISC-V or deployed-machine success claim.

External source remains GPL-2.0-or-later. Apache-2.0 covers only the original
packaging metadata, QA and documentation here.
