<!-- SPDX-License-Identifier: Apache-2.0 -->
# audiofile

audiofile 0.3.6 for openEuler 24.03 LTS SP3 riscv64/RVA23. The official
release archive is SHA-256 pinned and supplies the generated command and API
manuals expected by its build system. Frozen Arch, Debian, Fedora 44,
openSUSE, and Ubuntu lineage was cross-checked without executing recipes. The
complete upstream unit/format suite, including FLAC, the Linux ALSA example,
and an installed WAVE API smoke are mandatory. All installed manuals and
public headers, including `af_vfs.h`, have explicit RPM ownership, and the
spec declares the ALSA development dependency.
The build retains the internal static archive needed to link upstream's hidden
C++ unit-test symbols, then removes that archive from the installed package.
Apache-2.0 covers packaging.
