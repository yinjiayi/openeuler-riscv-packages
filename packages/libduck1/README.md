# libduck1

Daisy 2.02 talking-book metadata parser from the official v1.1.2 tag,
commit `d0ddd6bf9075199f546c5494f85512022a916a82`. All 38 Git files match
the SHA-256-pinned source archive. The historical AUR name `libduck1` is
retained; actual upstream library/SONAME/pkg-config names remain `libduck`,
`libduck.so.1` and `libduck` respectively. No upstream writes or patches.

The original default `./configure` and `make` build both static/shared
libraries and the unchanged `libduck-test.c` program. `--enable-pic` is
necessary for the shared library because upstream's architecture switch
predates RISC-V; neither library is disabled. Optional Doxygen output stays
at its original disabled default. There is no upstream assertive check target.

Downstream checks here mean additional acceptance assertions, not upstream
test cases: run the original program on an offline NCC/SMIL fixture and
compare all expected output, then compile shared/pkg-config and static
consumers, check book metadata, headings, two timed audio URI nodes,
navigation and rejection. Recompile/replay the original program against
staged and installed public headers/libraries. Original header/program
hashes are checked. Audio is referenced as metadata; no audio playback,
native hardware, timing or performance claim is made.

Complete original LGPL2.1 plus GNU GPL2/GPL3 companion texts are retained.
Original Debian GPL-3 packaging remains in the unchanged source archive,
not installed as binary-package content. Target provider primary/filelists
and recursive capability closure were checked against the official target
and current supplemental repository; no namespace/file collision was found.
These inert checks are not a successful DNF/build/install claim.

Hosted locked-image openEuler 24.03 LTS SP3 riscv64 RVA23 build/install and
independent physical RPM/SRPM/ELF acceptance remain required before merging.
No local upstream configure/make, RPM or QEMU execution, and no Auto-merge.
