<!-- SPDX-License-Identifier: Apache-2.0 -->
# LibTIFF

This directory packages the official LibTIFF 4.7.2 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The official OSGeo tarball is pinned by
SHA-256; archive inspection found a single `tiff-4.7.2` root, with no absolute
or parent-traversal paths. `LICENSE.md` contains the upstream libtiff license
and notices for bundled codec code. The Apache-2.0 header applies only to this
repository's packaging files.

The full upstream CTest suite runs in `%check`; no core tests are excluded.
The C and C++ libraries, tools, and available external codecs are built. The
release tarball's prebuilt HTML documentation is installed instead of running
Sphinx during RPM construction. The installed smoke test writes a TIFF via the
public C API, then reads it with both the public C API and `tiffinfo`.

The target's `libjpeg-turbo-devel` CMake package currently references a
missing `libturbojpeg.so.0.3.0` file. The upstream `jpeg-prefer-standard`
option selects CMake's standard FindJPEG path and retains JPEG codec support;
it does not omit JPEG tests or disable the codec.

The discovery snapshot corroborates LibTIFF in Arch, Fedora, and AUR metadata.
AUR is metadata only; no AUR build recipe is executed. QEMU-user CI can verify
functional behavior, but timing/performance or hardware claims require native
RISC-V evidence. A passing PR build does not imply RPM repository publication.
