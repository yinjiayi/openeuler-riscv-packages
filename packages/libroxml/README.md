# libroxml 3.0.2

This is the publisher-current 3.0.2 tag of the small C XML parser. The actual publisher homepage https://libroxml.net/ states “Lastest version is 3.0.2”; the frozen AUR 3.0.2-1 row is historical discovery lineage, not source acceptance. GitHub's only formal release is older 3.0.0: this package does not invent a formal 3.0.2 release. The official GitHub 3.0.2 tag points to ec1f9155471abb28724a21d14223a0467204aa04. Its tag and commit are unsigned; no available signature is skipped. The archive SHA256 is 8ee1af119c6054ef635e9d977b93e56b34ba7db62100012c9a3ece602c8691f7 and all82 ordinary files were byte-matched to the exact Git tree (93 archive members, no links/submodules).

## Rights and preservation

The upstream-authored debian/copyright explicitly grants Files:* LGPL2.1-or-later with the static-linking exception in License.txt, and overrides debian/* as GPL2-or-later. This is the recorded grant basis for the project's source, fixtures, PNG/SVG assets and templates, not an inference from merely finding a top-level license. LicenseRef-libroxml-LGPL-2.1-or-later-static-linking-exception names exactly that complete LGPL text plus its original leading exception, preserved as License.txt. This package extends the unchanged exception to the four declaration changes. The GPL2 document is supplied verbatim from the fixed official GCC mirror commit c9cd41fba9ebd288c4f101e4b99da934bcb96a11/COPYING, SHA256 231f7edcc7352d7734a96eef0b8030f77982678c516876fcb81e25b32d68564c, for the original Debian files. The added API driver has a complete ISC grant in its own source. Packaging does not relicense upstream or assert trademark permission.

All82 ordinary files are copied byte-for-byte into a separate source-notices tree before patching or bootstrap, with SHA256SUMS checked in target %check and installed smoke. The .notice suffix protects the preserved original paths from recursive configure helper updates. No upstream file, fixture, optional source or doc asset is pruned from the SRPM. Default documentation generation is OFF and stays OFF; no claim about ungenerated Doxygen output is made.

## Build and original checks

Autotools is the documented primary Unix build. Upstream autogen.sh bootstraps this Git archive, then plain configure and make retain shared/static libraries, roxml/rocat, float, thread-safe memory management, file parsing, edit, commit and XPath defaults. Docs, FUSE, tests, debug, verbose and compact/heap tuning retain their upstream default-OFF settings. Default install outputs, including libtool .la and static .a, are shipped. The default libtool 0:0:0 interface yields libroxml.so.0.0.0 with SONAME libroxml.so.0.

The original default make check is retained and has zero registered runtime cases. Additional QA reconfigures the same source tree with only --enable-tests after the default installation has been materialized. This avoids a blind out-of-tree build: configure probes relative unittest/unittest.c and the original runner reads relative fixtures. It builds all four original programs (normal, tiny, perf, mem) and executes the full unmodified normal and tiny runners. Each has34 registrations: --list must return34 and emit34 names, each full run must exit0 and emit34 OK lines without ERROR/FAILED. The tiny variant retains its original conditional test bodies; 34 registrations per variant do not mean68 distinct effective assertions. The perf/mem tools are compiled, not benchmarked; no performance or native-only validation is claimed.

RPM shell tracing is suspended outside each redirected original-runner/API
capture and restored before checking the retained raw streams. This prevents
shell trace commands from contaminating program stderr; genuine program stderr
must still be empty, list status/count must still be34/34, original full-run/API
failures retain their actual exit status, and no source test or assertion changes.
The first target attempt stopped at the list-stderr assertion after observed
status34 and34 names. Its stderr file was not retained, so trace contamination is
a shell-semantics inference, not a claim to have inspected those missing bytes.
Replacement target CI must validate all original and added runtime gates.

The sole patch changes four internal-header tentative definitions to extern; existing initialized .c definitions remain untouched. This addresses modern GCC -fno-common rather than relaxing that flag, disabling features or removing tests. It is a static diagnosis until actual target CI validates it.

## Added installed-library QA and limits

The added six cases cover buffer parsing/navigation, content/attributes, XPath result ownership, edit/exact serialization, temporary-file parse roundtrip, and specified NULL boundaries. They retain assert with -UNDEBUG and use six volatile function pointers. They do not prove full XML conformance, hostile-input security, concurrency, native timing or production suitability. Normal installed execution must have exact seven-line stdout and empty stderr; a separate LD_DEBUG run preserves its raw trace/SHA/failure status and proves all six exact driver symbols bind to the same installed libroxml.so.0.0.0 inode (not a brittle loader path spelling). All four installed ELF files must be RISC-V ELF64. The installed driver/source/fixtures manifest is generated after install-post stripping in %check.

No upstream compilation, bootstrap, tests, RPM or QEMU runs were executed locally during onboarding. Trusted repository metadata/tooling/source-verify-only gates are not target tests. The recipe requires no undeclared source fetch; actual CI containers are network-enabled and checksum-reverify their source cache, not proven network-isolated. Real target build, all original and added checks, physical notice/RPM/SRPM inspection, complete repository namespace, and protected-main publication remain independent gates.
