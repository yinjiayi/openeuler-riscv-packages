<!-- SPDX-License-Identifier: Apache-2.0 -->
# SDL2_image

This directory packages the SDL 2 image-loading library `2.8.12` as the
`SDL2_image` and `SDL2_image-devel` RPMs for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The package directory uses the inventory key
`libsdl2-image`; its RPM and development-provider names retain upstream's
`SDL2_image` spelling so consumers can resolve the expected library,
pkg-config module, and CMake package.

The official, non-prerelease GitHub release asset was independently downloaded
and verified with SHA-256
`393f5efb50536ec13ca4f4affb69cc9966d3c3f969e6c5e701faddf9f9785381`.
The archive contains one `SDL2_image-2.8.12` root and passed the repository's
path, link, member-type, and checksum checks before the target build.

The exact fixed openEuler repository metadata provides SDL2, SDL2's static
test-support library, and the libjpeg-turbo, libpng, libtiff, and libwebp
development packages. It does not provide libavif or libjxl development
packages. The build therefore enables all portable built-in image loaders,
uses strict system JPEG, PNG, TIFF, and WebP backends, keeps upstream's
default-disabled JPEG XL backend disabled, and explicitly omits the unavailable
optional AVIF backend. No vendored dependency fetch is used. `SDL2-static` is a
build-only requirement because upstream's registered tests link `SDL2test`; it
is not exposed as a runtime dependency of either output RPM. Upstream's sample
programs are compiled, and its complete registered test executable runs
serially with every shipped fixture under SDL's dummy video driver. The
installed smoke test compiles and links through the pkg-config development
interface and decodes a PNG through the installed shared library. The CMake
configuration remains packaged, while the smoke environment intentionally does
not add CMake as a runtime dependency of `SDL2_image-devel`; the complete
upstream CMake-built test suite still runs during `%check`.

Target CI retains outbound network access, but every source byte remains bound
to the committed SHA-256 before `rpmbuild`. Ubuntu GA metadata supplies the
frozen inventory lineage; no Ubuntu build recipe, AUR recipe, or other external
distribution packaging code is read or executed.

External sources remain under their upstream Zlib license. Apache-2.0 covers
only this repository's original packaging metadata, scripts, and documentation.
