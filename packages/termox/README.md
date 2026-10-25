<!-- SPDX-License-Identifier: Apache-2.0 -->
# termox

Packages TermOx 2.0.0, preserving its static library, full default CMake graph,
and original two explicitly selected unit registrations. Both original test
bodies are empty or comment-only: their successful runner exit is not functional
test coverage. Five original examples and dependency tests remain available as
upstream EXCLUDE_FROM_ALL targets; this recipe does not disable them or claim
they ran. Escape and zzz require C++20 despite the former C++17 package summary.

All four official immutable archives are SHA256 pinned and source/Git-tree
matched. Available TermOx commit signature was independently verified as a
GitHub web-flow attestation, not an author-owned release signature; the three
dependency commits have no available signature. Sources and dependencies remain
MIT under their original complete project grants. All 55+19+43+9 ordinary source
files are preserved verbatim as .notice files plus SHA256SUMS before configuration,
including every grant, copyright, README and original test. They are not treated
as new packaging code or relicensed by this repository.

Configuration is unprivileged and offline using explicit FetchContent source
overrides; no original sources or defaults are patched. Global ox headers and
libTermOx.a retain their original installed names. Exact dependency headers live
only below /usr/include/termox/third-party, and libescape.a below /usr/lib64/termox.
The upstream signals-light global install rule is not invoked. termox.pc exposes
the private headers/static archive and ICU dependency link flags to consumers.

Six additional noninteractive API cases cover ScreenBuffer allocation/fill,
mutable/const indexing, Canvas translation, resize-then-fill, Unicode conversion
and invalid UTF8, and signal disconnection/lifetime. The test never constructs a
Terminal or Timer and makes no terminal I/O, authentication, latency, security or
arbitrary-Unicode safety claim. Installed QA compiles the preserved API source
against installed package-owned static archives, verifies both archives in the
actual linker map, reads RISC-V ELF headers, executes all six cases, and checks
that deliberately omitting TermOx fails to link with unresolved ox symbols.
Static archive evidence is not a dynamic LD_DEBUG symbol-binding claim.

No target build or functional QA has been run on the local Codex host. New-head
target CI, actual RPM/SRPM/notices and complete repository namespace acceptance
remain required after the guarded package-only repair push.

Installed termox.pc also declares -std=c++20, so consumer compilation tests the
actual pkgconfig language contract. Prep explicitly uses declared tar/gzip;
%setup precedes verbatim notice preservation, then %autopatch (currently empty).
Additional API stdout must byte-match seven expected lines (six cases plus
summary), with exit0 and empty stderr at both build and installed stages.
Installed positive-link failures preserve and print real status/raw diagnostics.
Target ar/nm/readelf/link-map assertions require the original terminal.cpp.o and
transcode.cpp.o members and their selected defined symbols, not just arbitrary
archive presence. These are future CI assertions, not local target results.

The exact stdout comparator cmp is supplied by explicitly declared diffutils at build and installed-test roles, not presumed to belong to coreutils.
