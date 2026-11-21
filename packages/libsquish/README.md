# libsquish 1.15

The official SourceForge `libsquish-1.15.tgz` archive is fixed at SHA-256
`628796eeba608866183a61d080d46967c9dda6723bc0a3ec52324c85d2147269`.
The current official file listing was rechecked for this intake and publishes
that digest; 1.15 is its highest numbered published release. No detached
signature was listed, so this is not a signature-verification claim. Frozen
discovery lineage includes Arch extra 1.15-8, Debian stable/main 1.15-3,
Fedora Everything-source 1.15-21.fc44, and Ubuntu resolute/universe 1.15-4.
The recipes of those distributions were not executed or copied.

## Rights and provenance

The archive has 54 ordinary source/build/documentation/artwork/revision files.
31 contain the complete original MIT grant and disclaimer, equal to root
LICENSE.txt after whitespace normalization. These include Simon Brown's
copyright and Ignacio Castano's 2007 changes in clusterfit.cpp/clusterfit.h.
The remaining 23 are associated project files under the root MIT software and
associated-documentation grant; no independent per-file grant is invented.
All 54 exact original members are copied with a `.notice` suffix before the
package patch and retained in the license tree with a SHA-256 manifest.
Original PNG/SVG assets and embedded metadata are preserved, not regenerated.
The SVG refers to font-family names but embeds no font program. ChangeLog.txt
attributes the SVG contribution to Stefan Roettger. This does not assert an
independent font license or permission to use project trademarks.

## Original defaults and portability patch

Use the upstream preferred CMake build. Preserve its original default static
library, OpenMP ON, Altivec OFF, and extras OFF. Build a second isolated shared
variant as an addition, not a replacement of the default static library.
Both complete upstream library/header install sets are installed, with the
original literal `lib` install directory relocated to target `lib64`.
The unused GNUmake .pc template has a stale version and incorrect link name;
the original CMake install does not install it, and this package does not
present it as valid pkg-config metadata. CMake does not build Doxygen docs by
default; no original default documentation feature is disabled.

Patch `0001-default-sse2-only-on-x86.patch` is a package-authored MIT portability
fix against 1.15 CMakeLists.txt. Its unconditional SSE2 default adds `-msse2`
on Unix even for non-x86 targets. Only the option's default is made dependent
on CMAKE_SYSTEM_PROCESSOR: x86 keeps SSE2 ON; other processors select the
already supplied scalar backend. Explicit option overrides, original x86
SIMD code, OpenMP and other defaults remain intact. This is a general
architecture-default fix, not a new RISC-V codec or a performance claim.
It is not submitted upstream. Remove it when a verified newer official source
selects architecture-compatible defaults with the same feature semantics.
Metadata records the package-local patch and full digest; the SPEC applies it
explicitly after preserving original notices.

## Test and execution boundaries

Original CMake registers **zero default runtime test cases** and no `check`
target. No fictitious upstream test success is claimed. Optional
extra/squishtest.cpp is retained unchanged; it is not enabled by the upstream
default and prints compression statistics rather than enforcing an asserted
quality threshold. This package does not disable or delete an original test.

Six additional strict functional cases exercise documented positive arguments:
DXT storage sizes including partial dimensions; exact DXT1 black; DXT3/DXT5
alpha endpoints; a 5x5 image with canaries and zero error for exact black; and
independently specified opaque/transparent DXT1 wire blocks. Assertions are
explicitly enabled after RPM optimization flags. The same cases execute
against the intact default static archive and the supplemental shared library
in target `%check`. The installed driver is replayed and six exact C++ APIs
must bind from that absolute installed driver to the same installed library
file, accepting legitimate `/lib64/lp64d` aliases by file identity, not a loose
path substring. The actual exported symbols are selected by exact demangled
signatures from the installed ELF. Driver/source post-strip checksums, all 54
notice checksums, raw loader trace, trace hash and real failure status are
retained. Loader environment contamination is cleared before installed replay.

Local checks are trusted repository validation/tests/golden evaluation, inert
source/patch/provider inspection and source verification only. They do not
compile or execute upstream code, and do not establish target RPM, codec,
installation, timing, performance, security or native hardware acceptance.
Actual target CI must build/install and execute the committed checks before
physical RPM/SRPM, complete namespaces and current-head merge acceptance.
The recipe requires no undeclared network fetch; actual CI bridge networking
is independently configured, and no offline-isolation claim is made here.

## Dependencies and names

The complete fresh official openEuler primary/filelists join supplies CMake,
GCC/G++, OpenMP libgomp/compiler headers, standard C/C++ headers and every
declared command, with versioned transitive closure. This static metadata
proof is not a DNF/SAT transaction result. The full official namespace has no
component identity or owned-path collision. Two broad `squish` alias hits are
unrelated ActiveSupport String-method documentation, explicitly retained and
dispositioned in the external intake receipts rather than silently erased.
Fresh canonical/all-open deduplication is separate from supplemental published
repository namespace acceptance, which must also be verified before merge.
