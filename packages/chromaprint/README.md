<!-- SPDX-License-Identifier: Apache-2.0 -->
# chromaprint

This directory packages Chromaprint `1.6.1` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. GitHub marks `v1.6.1` as the publisher's current stable
release and supplies the immutable release asset recorded here. Its SHA-256 is
pinned. The 481-member archive has one root, no unsafe path or special member,
and one safe in-root relative symlink (`src/include/chromaprint.h` to
`../chromaprint.h`).

Frozen Arch stable, Fedora 44 GA, openSUSE Tumbleweed, Debian stable, and
Ubuntu 26.04 LTS GA metadata corroborate the component. Read-only AUR RPC found
no exact AUR package; no AUR PKGBUILD or distribution packaging recipe was
read or executed. The canonical component is `acoustid.org-chromaprint`, which
also matches the reviewed discovery registry.

The source combines Chromaprint's MIT implementation, bundled
LGPL-2.1-or-later FFmpeg resampling code, and BSD-3-Clause test/FFT code. The
distributed library links the fixed target's GPL-2.0-or-later FFTW3 library,
which is included in the binary-license expression. The internal resampler is
retained because disabling it changes tested audio conversion behavior; the
external FFT backend is fixed to FFTW3 to match the existing target build.

The fixed target currently carries source package `chromaprint-1.5.1-1` and
binary packages `libchromaprint` and `libchromaprint-devel`. This `1.6.1-1`
update has a higher EVR, retains `libchromaprint.so.1`, preserves all 22 prior
public `chromaprint_*` symbols, and adds two APIs without removing an old one.
No installed reverse consumer was found in the fixed repository metadata. The
`ffmpeg-devel` and `fftw-devel` BuildRequires close against that same SP3
`riscv64` repository set.

`%check` registers and runs the complete upstream suite with tools enabled,
including the FFmpeg reader fixture: 100 of 100 tests pass with no skip or
failure. Installed smoke verifies `fpcalc`, SONAME and pkg-config metadata,
compiles and runs a public C API consumer, generates raw audio, and obtains a
fingerprint through the installed command-line tool.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
