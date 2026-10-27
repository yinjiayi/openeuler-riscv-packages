# Grepcidr 2.0

This is Jem Berkes's original PC-Tools component, not John Levine's independent
grepcidr-2 fork. The actual publisher page calls 2.0 the most-current official
release (2014-05-26); the source version agrees. ChangeLog's entry date differs
but is retained verbatim. Immutable catalog rows 21050 and 172648 remain lineage
only; no PKGBUILD, distro script or upstream instructions were executed.

Official source: https://pc-tools.net/files/unix/grepcidr-2.0.tar.gz
SHA-256: `61886a377dabf98797145c31f6ba95e6837b6786e70c932324b7d6176d50f7fb`.
The exact 16,557-byte archive also matches the actual offered SHA-512 sidecar.
That is an unkeyed digest, not a digital signature. No Git repository, detached
PGP signature or global absence of signatures was invented. The URL remains
mutable; current publisher source/identity must be re-fenced before submission.

All seven original files are preserved byte-for-byte in source-notices before
patching, including GPL2 COPYING, original C and GPL2-or-later DocBook/manual
grants and Jem Berkes/Ryan Finnie/John Levine credits. Independent packaging
and added shell QA are Apache-2.0 with the complete legal text shipped. Raw
opensuse/oss discovery labels are mapped only to schema opensuse-tumbleweed;
this neither imports a new distribution nor changes frozen source evidence.

The package-only patch defines unsigned IPv4 shifts and ctype inputs, checks
pattern/line allocation growth, preserves final non-newline text at allocation
boundaries, recognizes the legal all-zero IPv6 hint, and honors linker flags.
These are static source findings, not observed crashes, CVEs or general safety
claims. It retains all options, features, default scanning, -O3/-Wall/-Werror,
original all/install and the supplied manual. The optional doc target is kept;
it is not invoked because the release already supplies its installable manual.
No upstream check/test target or registered test program exists; none is
silently omitted or called a successful upstream test suite.

Added QA has six logical groups (multiple exact status/stdout/stderr checks):
version's original exit2; unsigned IPv4 /0,/1,/24,/32; IPv6 including default
::/0; pattern files/overlap/hints/x/invert/include/count; 8193 patterns per IP
family; EOF511/1023 without newline, long line, non-ASCII prefix and exit bounds.
Allocation guards are reviewed statically, not memory-fault-injected. Build
and installed-RPM runs use the same owned helper; empty-stdin is explicitly a
no-match, not functional success. Installed QA verifies the actual ELF64/RISC-V
binary, libc dependency, no RPATH, same-file identity and final post-strip
payload/source-notice hashes, retaining raw logs on success and failure.

No local upstream/target compilation or execution occurred while preparing this
recipe. Exact-head target CI, full physical RPM/SRPM and current provider/source
identity/namespace acceptance remain required; no network traffic, native ISA,
security or performance assurance follows. No shared CI/catalog modification,
upstream write or full Daily discovery coverage is claimed.
