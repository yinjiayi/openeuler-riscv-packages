# libabw 0.1.4

The fixed release comes from The Document Foundation's official libabw release
index, whose current listing contains 0.1.4 (26 May 2026) and no higher version.
The original archive is SHA-256 pinned; it contains 97 ordinary files.
Frozen Arch/openSUSE discovery rows independently establish package lineage,
not the current upstream version or target availability.

## Original behavior and tests

Plain configure retains the original Unix defaults: shared library enabled,
static library disabled, all three conversion tools enabled, API documentation
enabled, fuzzers disabled. Doxygen and Graphviz are declared build dependencies.
The original make/check graph is retained. It registers zero upstream runtime
test cases; that is not counted as functional test coverage.

Six added assertion-driven cases cover null input, accepted AbiWord/awml roots
and stream reset, invalid roots/namespaces, plain XML-to-text streaming,
gzip-to-identical-text streaming, and rejection of the single invalid XML
opener "<". The original XML reader enables recovery; the last case does not
assert that all truncated or malformed documents must be rejected. Only the driver
uses -UNDEBUG, after normal RPM flags; library hardening/defaults are unchanged.
The synthetic fixture and driver source are included with a manifest of the
actual post-install-post/stripped helper bytes. Build and installed checks also
verify real text-converter output, not only a CLI exit status.

The installed replay clears loader override variables, retains the complete
LD_DEBUG trace and checksum even on driver failure, and verifies both exact
public C++ symbols bind from the absolute installed driver to the same file as
libabw-0.1.so.1.0.4. Filesystem identity checks permit legitimate loader aliases
such as /lib64/lp64d; no hard-coded loader path spelling is assumed.

## Documentation installation correction

The one generic packaging patch changes only the paired documentation install
targets in Makefile.am/Makefile.in. Three extension globs become a recursive
copy of the complete generated HTML tree into the same destination. This
preserves JS, SVG, font, nested assets and their embedded notices, and avoids an
unmatched PNG glob. Configure, all, check, parser sources and documentation
generation are unchanged. No feature or original test is disabled.

## Rights and provenance

Core library/tools carry MPL-2.0. The token generator's explicit
MPL-1.1/GPL-3.0-or-later/LGPL-3.0-or-later choice is exercised as GPL-3.0-or-later.
GNU helpers retain their full GPL-2.0-or-later or GPL-3.0-or-later configuration
exceptions; libtool retains its output exception. Full GPL version 2 and 3
texts are separately fixed to immutable GCC Git objects. Macro/automake
permission notices (FSFAP), embedded MIT alternatives, and the install-sh X11
name-promotion restriction are retained. Unmarked project build/resource files
are documented in the release's complete MPL context, without inventing
independent per-file grants.

Before patching or RPM configure helper refresh, all 97 original members are
copied verbatim under license-notices with non-matching .notice suffixes.
Their full path/copyright/exception text is preserved, together with both GPL
texts, in a 99-entry SHA-256 manifest checked during build and installed replay.
The SRPM retains all three pinned inputs and the patch.

The source-member inventory does not establish licensing of future generated
Doxygen assets. All generated assets and embedded notices are installed
unmodified. Actual generated JS/CSS/fonts/images, their tool-supplied notices
and any needed additional legal text remain a mandatory physical CI review
before merge; no claim of complete generated-asset acceptance is made here.

## Evidence boundary

Target is openEuler 24.03 LTS SP3 riscv64 RVA23. Full retained official
primary/filelists metadata are freshness-bound and used for declared dependency,
command/header and namespace projection. The transitive static provider
projection is not a DNF solver result or supplemental-repository acceptance.
The recipe needs no undeclared fetch; the trusted CI bridge is network-enabled,
so this is not an offline-isolation claim.

Local work executes only trusted repository validation/tool tests, golden
fixtures, metadata/schema/syntax checks and source verification-only. No
upstream compilation/test, RPM build or QEMU/target program is run locally.
Those checks do not establish parser correctness or successful target build,
installation, native behavior, security/fuzz resilience or physical artifacts.
Fresh exact-head target CI and independent artifact/license/namespace review
are required before merge.
