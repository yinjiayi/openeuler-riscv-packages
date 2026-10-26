<!-- SPDX-License-Identifier: Apache-2.0 -->
# libblip-buf

This directory packages upstream `https://gitlab.com/TASVideos/libblip_buf` version `1.1.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Official release1.1.1 is bound to commit8f5101b1d3229657ce71c2d395e78c8ad69f2cb1.
Source0 is the fixed official GitLab commit archive, SHA256
6f07ea138d0e23c1d376c3cae69d3180384e9cc0eb5ef9fe641834c0e70f2162.
All8 ordinary archive files match the full immutable Git tree. The original
release attachment, obtained through the actual API-rendered upload link,
SHA256915f98b7c0ecefd00adb18b883728d642ac3fef0d51412332d92638f14da777f,
contains exactly the same8 files byte-for-byte, not an omitted fuller test suite.
Tag/commit signature endpoints returned404; this is not signature verification
or proof of universal signing-type support. No offered signature was returned.
The stale AUR discovery row remains unchanged; current official release bytes,
not historical catalog metadata alone, establish this normalized component.

License: LGPL-2.1-or-later, explicitly granted by Shay Green2003–2009 in
blip_buf.c with the complete LGPL2.1 in license.txt. All original files,
including historical Makefile/docs, are retained verbatim as source-notices in
the binary package and as corresponding source in the SRPM. No source patch.

The actual Makefile's default all builds both dll and so. Both are built with
PIC/RPM flags and SONAME libblip_buf.so.1; blip_buf.dll is target Linux ELF,
preserved under the private lib64/libblip-buf directory, not Windows support.
There is no upstream install/test/check target. Historical makefile_orig and
README mention demos/tests that are absent in both official artifacts; no
upstream suite success is claimed, and no provided test is removed or replaced.

Additive QA compiles against staged installed headers/shared library, checks6
bounded API contracts (allocation, rates/counts/clear, partial mono silence,
stereo stride, normal/fast deltas) and10 exact same-file dynamic symbol bindings.
It is rerun after RPM installation. Driver/helper source checksums and complete
loader traces are retained. This is not a reference-audio/fidelity/performance,
device, native RISC-V or general memory-safety claim. No local source/RPM/QEMU
build has been executed; real target build/install remains CI's gate.

Audited dependency/namespace projection uses complete official18503 packages
and fixed M157 supplemental1588 binary/495 source packages; it is not DNF SAT
or actual future RPM payload acceptance. New PRs remain unmerged until current
main/exact-head/full required CI and physical RPM/SRPM/source/install gates pass.
