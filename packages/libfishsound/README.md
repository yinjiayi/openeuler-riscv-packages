<!-- SPDX-License-Identifier: Apache-2.0 -->
# Libfishsound

This directory packages Xiph's official Libfishsound 1.0.1 release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The downloaded HTTPS tarball's
SHA-256 matches Xiph's published release checksum. Archive members have one
root directory and no absolute or parent-traversal path. The source is
BSD-3-Clause; Apache-2.0 governs only this repository's packaging files.

The target's available Vorbis, Speex, and FLAC development packages are all
required. The SPEC checks that configure actually enabled every codec and
both encode/decode paths. The complete upstream `make check` suite runs
serially; the installed smoke test creates and destroys public API handles
for all three codecs. Source-bundled Doxygen HTML is installed without
requiring a documentation regeneration during RPM construction. The optional
liboggz example utilities are not installed by upstream and are not used as
evidence for the codec library.

The immutable discovery snapshot corroborates the component in Arch,
Debian, Fedora, openSUSE, and Ubuntu. No external packaging recipe is
executed. QEMU-user CI verifies functional behavior only, not native RISC-V
timing or performance. PR build success is not publication evidence.
