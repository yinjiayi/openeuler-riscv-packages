# libjodycode 4.2

The official Codeberg release is explicitly **v4.2 Stable**, dated 2026-10-20.
Its lightweight tag points to commit
`64bca2874f895df98003f8bf4ca267dd6926b17f`, tree
`4f5ca67a815b1885118e7f04ce8b849445fed6cc`. Every one of the 81 ordinary
source files matches its Git blob; the archive digest is pinned. The source
URL is tag-based and therefore mutable: fixed bytes and before/after ref
fences are evidence, not a claim of immutable publisher URL or signature.
Neither actual tag nor commit offers a PGP/SSH signature, so no key is guessed.
Genuine frozen Arch/Debian/Fedora/openSUSE lineage is retained, advanced from
its historical 4.1.2 cue by actual upstream release evidence. Tags page1 only
contained 10 of 17 tags; that observation is not called a full history scan.

The same release object's CHANGES/release body says feature level5, while its
actual header/exported constants say **4.2.0, API4, feature level6**. The recipe
does not alter or hide this discrepancy. It ships the actual full file
`libjodycode.so.4.2.0` with original SONAME `libjodycode.so.4` and checks actual
header/binary values, not the stale release-text number.

## Rights and defaults

All 81 source members, including hidden files, scripts and skeleton examples,
are copied byte-for-byte into `license-notices/<relative>.notice` before the
patch. Their SHA256SUMS is checked during build and after installation. The
complete project MIT text is retained. The unmodified skeleton has MIT terms
and an additional optional permission to relicense modified projects; this
package does not exercise that permission. Four source members explicitly
declare public-domain release by Jody Bruchon: the c99_aligned_alloc pair,
likely_unlikely.h and helper_code/libjodycode_apiver.c. For the c99 pair the
explicit PD branch is selected, not an invented fetched CC0 document. The
LicenseRef is defined by these complete original notices and accompanying
Public-Domain.notice. New QA/packaging uses Apache-2.0 with full legal text.
Windows resource XML/API references are preserved original source, not a claim
of Microsoft binary distribution or Windows validation.

Original `make all` builds the manual, shared library and static library.
Original `make install` installs both libraries, one header and compressed
section3 manual; there is no upstream pkg-config module or CLI to invent.
Original GNU11, no-LTO defaults remain. Existing upstream uname/compiler guards
select the portable non-x86 hash implementation on RISC-V, retaining the x86
SIMD path for x86 builds; no blanket SIMD/C99/LTO feature override is added.
RPM flags use CFLAGS_EXTRA and environment LDFLAGS so the Makefile retains its
own compiler options and SONAME append instead of suppressing them through a
command-line LDFLAGS override.

Original `make test` is retained unchanged. It runs the original 90-byte
dummy script that only prints OK: **zero upstream functional assertions**,
not meaningful functionality evidence. Nondefault kernel/cache probes and
the filesystem-specific REFLINK example remain in the original source/targets
but are not run or claimed to pass. No kernel/native timing/cache performance,
filesystem-dedup safety, cryptographic security or Windows behavior is claimed.

## Narrow repairs and strict added cases

One generic two-file patch initializes the successful relative-path return
value and continues numeric comparison after equal case-folded characters.
Both were found statically, not by a local compiler or RISC-V execution.
Original source/default targets remain; remove the patch once upstream has
equivalent fixes and regressions. The added asserted cases cover:

1. Actual ABI/header values and strtol conversion/overflow/NULL errors.
2. Normal, tail and rolling noncryptographic hash versus a target-run reference
   recurrence; this is consistency evidence, not independent cryptanalysis.
3. Numeric ordering, Ab2/ab10 casefold-suffix regression, equality and NULL.
4. Owned length-prefixed C strings, zero-for-equality and size guard.
5. Absolute collapse, relative path success, identical path and NULL status.
6. Binary temporary-file roundtrip, EOF and invalid NULL/EFAULT behavior.

The source build exercises the same consumer against the built shared library.
Installed smoke recompiles from the installed header in a fresh temporary
directory, with explicit runtime GCC/glibc-devel. A no-library link must fail
for all six anchor functions and leave no executable. The positive consumer
must need SONAME `.so.4`, have no RPATH/RUNPATH, and pass exact six-case stdout
with empty stderr. A separate LD_DEBUG run is parsed for exact normal-symbol
caller/target identities; every selected caller must be the temporary absolute
consumer and every target must be `-ef` the actual installed `.so.4.2.0`, allowing
real loader aliases. Raw status/stdout/stderr/trace, canonical paths and hashes
are retained in logs even on failure. Data constants are checked by value,
not a directional binding assertion vulnerable to ELF COPY relocation.

The installed manifest is produced in %check after RPM install-post. No local
source/compiler/RPM/QEMU execution provides target evidence: actual target
build, original dummy invocation, six functional cases, installed consumer,
full products/namespace and publication remain independent required gates.
