# libsubprocess 2.5

This package supplies the original `cpp-subprocess/subprocess.hpp` header and the
repaired original CMake target/configuration export. It does not invent a shared
library, static archive, pkg-config module, command-line tool or prebuilt QA binary.

## Source and rights

The selected official formal release is `v2.5` (release246362665), fixed to commit
`60d4ad8d528173a2e4c98fd64aa9191728832355`. Source0 is the exact official GitHub
commit archive, SHA256 `f2c947e0dcfd800652275d6f7deb76d155a953a1a5df969383530445f01c29eb`.
All27 regular files match the full Git tree's blob IDs and executable modes.
The complete MIT grant credits Arun Muralidharan (2016–2018). The original
27-file notices/raw hashes are copied before patching, including two unused
x86_64 Mach-O source artifacts: neither is installed or executed. Original
packaging and owned QA use Apache-2.0 with its full legal text also shipped.

The offered commit PGP signature was independently reconstructed and verified
with the current REST-linked GitHub `web-flow` certificate, full fingerprint
`968479A1AFF927E37D1A566BB5690EEEBB952194`. This proves that precise GitHub
signed-commit attestation; it is not an archive detached signature, a personal
author signature, or a universal source-security claim. The archive's calculated
SHA256 and complete Git binding remain separate checks.

## Preserved behavior and scoped repairs

Upstream's CMake project says2.2 and header documentation says1.0.0 despite the
formal2.5 release. The package records that mismatch and repairs the CMake
project/export version to2.5. Its package-local patch fixes the existing export
paths/GNUInstallDirs/minimum FILE_SET capability and keeps the original ten
CTest registration bodies. A build-tree copy supplies the header path expected
by an existing original piping test; it does not substitute a test suite.
The header repairs are bounded: empty joins/commands, length/error propagation,
stderr redirection and complete draining, and stream-move communication binding.
These are source-derived correctness findings, not observed CVEs or native failures.

Original CMake tests and installation default OFF. Packaging explicitly enables
both and runs all ten original CTests with assertions active. It then compiles
an additive consumer through the actual exported CMake package and installed
header, testing ten exact groups: joins, empty commands, stdout, large stderr,
two-pipe status, stderr redirection, bounded startup errors, threaded read errors,
empty buffers and moved streams. Timeouts are failures, not successful coverage.
The installed consumer is compiled afresh in target CI; no prebuilt QA executable
is shipped. Header/helper/source hashes, include traces and ELF/RISC-V/no-RPATH
checks bind the installed exercise to the actual payload, not an ambient source tree.

## Target and maintenance boundary

The target is openEuler24.03-LTS-SP3 riscv64/RVA23. Active Linux code uses POSIX
process/file APIs and C++11/pthreads; no observed architecture assembly justifies
a native-only classification. Windows code remains in source without a Windows
portability claim. CMake>=3.23, gcc-c++ and all original test tools must be
closed by full current provider/namespace evidence before submission.

Updates use the observed official GitHub releases API and strict numeric
`vX.Y[.Z]` tags; the current source entry remains pinned to the complete commit.
Discovery retains the exact AUR2.5-1 row and frozen snapshot lineage, not an AUR
recipe execution or a new catalog-wide scan. Metadata validation/tool tests,
source verification, target compilation/original CTests/owned consumers, physical
RPM inspection, namespace acceptance and publication are distinct gates. This
proposal does not assert any unrun target result, full Daily coverage, native,
performance, loader-equivalence or general security correctness.
