<!-- SPDX-License-Identifier: Apache-2.0 -->
# SDL2_image

This directory packages the SDL 2 image-loading library `2.8.8` as the
`SDL2_image` and `SDL2_image-devel` RPMs for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The package directory uses the inventory key
`libsdl2-image`; its RPM and development-provider names retain upstream's
`SDL2_image` spelling so consumers can resolve the expected library,
pkg-config module, and CMake package.

The official, non-prerelease GitHub release asset was independently downloaded
twice and both copies had SHA-256
`2213b56fdaff2220d0e38c8e420cbe1a83c87374190cba8c70af2156097ce30a`.
The current official SDL 2 tag feed also exposes `2.8.12`; this package remains
at the task-selected inventory version `2.8.8`, while update metadata retains
`2.8.12` as the latest detected SDL 2 release instead of claiming the frozen
inventory value is still newest upstream.
The archive contains one `SDL2_image-2.8.8` root, only regular files and safe
relative symbolic links, and no absolute path, parent traversal, unsafe link,
or special-file entry. Its detached signature names upstream fingerprint
`1528 635D 8053 A57F 77D1 E086 30A5 9377 A776 3BE6`; the build records that
signature as advisory and does not claim a cryptographic verification.

The exact fixed openEuler repository metadata provides SDL2, libjpeg-turbo,
libpng, libtiff, and libwebp development packages. It does not provide libavif
or libjxl development packages. The build therefore enables all portable
built-in image loaders, uses strict system JPEG, PNG, TIFF, and WebP backends,
keeps upstream's default-disabled JPEG XL backend disabled, and explicitly
omits the unavailable optional AVIF backend. No vendored dependency fetch is
used. Upstream's sample programs are compiled, and its complete registered
test executable runs serially with every shipped fixture under SDL's dummy
video driver. The installed smoke test exercises both the pkg-config and CMake
development interfaces and decodes a PNG through the installed shared library.

Target CI retains outbound network access, but every source byte remains bound
to the committed SHA-256 before `rpmbuild`. Ubuntu GA metadata supplies the
frozen inventory lineage; no Ubuntu build recipe, AUR recipe, or other external
distribution packaging code is read or executed.

External sources remain under their upstream Zlib license. Apache-2.0 covers
only this repository's original packaging metadata, scripts, and documentation.
