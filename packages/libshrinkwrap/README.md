# libshrinkwrap

The official C++ header-only shrinkwrap v1.2.0 release is fixed at
`eaac292b255b5de45d6546a794ffbd103335bc40`. All 14 original regular Git blobs
match archive SHA-256
`f6fd4275629effc6eef8aa5c3b1eedcb5c03294d7c70585c4ccecd0ca7b63dbd`.
Discovery lineage is `discovery-20260808T165000Z-9a89920c269462cd`, AUR
libshrinkwrap 1.2.0. No AUR recipe is executed or copied.

This is unrelated to the target's Java org.jboss.shrinkwrap 1.2.6 RPM.
The RPM name is libshrinkwrap, with no generic `Provides: shrinkwrap`;
C++ header/CMake paths and capabilities were independently checked against
complete official and supplemental primary/filelists metadata. All build and
consumer dependencies are supplied; metadata closure is not real DNF evidence.

Original MIT sources/notices stay unchanged. The unused `dep/zstd.cmake` has a
separate BSD notice and refers to missing LICENSE/PATENTS. Complete official
zstd v1.1.4 companion texts are additional fixed inputs; its BSD LICENSE is
byte-identical to the v1.3.2 license named in original requirements. PATENTS is
retained as historical text because v1.3.2 no longer includes it. This does not
assert patent clearance or build a bundled old compression library. System
zlib, liblzma and zstd supply all three backends offline. No backend is disabled.

The upstream CI enables `BUILD_TESTS=1` and Debug, so the recipe does too:
all 11 original registered CTest commands and the original test source are
preserved, with assertions enabled. Original random seek seeds remain random;
failure sequences are printed by upstream. Staged and installed CMake consumer
replays compile the unchanged original test source and run the same 11 commands,
checking original header/test SHA-256 and CMake include-prefix relocation.
Those two replays are not two new upstream suites. Original optional cget files
remain in the source archive but are not executed or used to download dependencies.

Only headers, CMake metadata, source tests and documentation are installed,
therefore the RPM is noarch and debug subpackages are inapplicable. Target
compiler/runtime behavior still requires the locked openEuler riscv64 CI build,
all original tests, actual RPM installation, smoke and physical RPM/SRPM
acceptance. No local upstream/target execution, Auto-merge, native, timing,
performance, security or publication success is claimed.
