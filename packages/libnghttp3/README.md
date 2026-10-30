# libnghttp3

Canonical package `libnghttp3` packages the official ngtcp2/nghttp3 v1.18.0 release.
The authenticated release archive is used rather than a Git archive that omits
bundled MUnit. The fixed commit is dbfc24286138cb0b6490160e7ca87fe1ce6722a0.
Release SHA256 is 2812e9c06583fa24c8dc46bdb5291310a69196352ceaca8fbe98106ff36ae7d8.
The archive has 120 main-Git-identical files, generated ChangeLog and 24 build
extras, and 6 files matched to exact bundled sfparse/MUnit Gitlink commits.
Thirty-one main-tree files are absent, explicitly including optional documentation
generators and fuzz/maintenance inputs; this is not an all-Git-files archive claim.

The compiled library and bundled sfparse/MUnit carry full MIT grants. The SRPM
also retains generated GNU tools/macros. GPL3 is elected where a GPL2-or-later
choice exists, preserving each Autoconf/Libtool/output exception. This does not
make the compiled library GPL. install-sh retains the complete X Consortium
permission/name restriction and FSF public-domain notice. MUnit's clock snippet
retains the explicit portable-snippets CC0 waiver. The LicenseRef identifies
that exact waiver, not an invented umbrella grant. All 151 original raw files are
shipped unchanged as hashed source-notices; full GPL3 and Apache2 texts accompany
it. Owned downstream packaging and QA are Apache2. No original source is patched.

CMake production defaults remain enabled: shared/static libraries, C++17 qpack
example and testing. Original check builds main then invokes unfiltered CTest;
this recipe builds that same main and invokes CTest once with verbose reporting.
Its one CTest test contains 8 MUnit suites / 61 registrations, including 100000
seeded Huffman roundtrips of 100 bytes each. No test selection, short-loop patch,
assertion removal or network/TLS/QUIC dependency is introduced. Optional AVX2 is
not enabled. GCC >= 15 is documented as known to work, not a source configure gate;
target GCC 14 compatibility is not claimed before target CI.

Installation preserves 2 public headers, the `.so.9.9.0`/SONAME9 library and static
archive, libnghttp3.pc, and upstream's literal `/usr/lib/cmake/nghttp3` exports.
The qpack example is built but not installed, matching upstream. Private installed
QA freshly compiles the same 6 public-API groups against pkg-config shared linkage
and the actual installed static archive. It retains negative-link diagnostics,
GNU link maps/traces, ELF/NEEDED/SONAME checks, 11 exact same-file loader bindings
and before/after hashes. This is user-mode API/package evidence, not HTTP/3 network
interoperability, native hardware, security, performance or full Daily coverage.

Source authentication, full namespace/provider joins, target builds/default tests,
installed physical proof, merge and independent publication are separate gates.
This proposal itself does not establish any target execution or delivered PR.
