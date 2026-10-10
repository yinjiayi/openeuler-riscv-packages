<!-- SPDX-License-Identifier: Apache-2.0 -->
# SFML 2.x compatibility provider

This directory packages SFML 2.6.2 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. “Compatibility provider” means that the RPM deliberately keeps
the SFML 2 public API and ABI for consumers that cannot yet use SFML 3; it does
not claim to be the latest upstream major series. The frozen inventory's
canonical `sfml-dev.org` record includes AUR `sfml2` 2.6.2, Debian `libsfml`
2.6.2, Fedora `SFML` 2.6.2, and openSUSE `sfml2` 2.6.1. Independent official
GitHub tag and release checks establish 2.6.2 as the newest stable 2.x release.
AUR was used only as frozen read-only metadata; no PKGBUILD or external
packaging recipe was read or executed.

The official `2.6.2` GitHub tag archive is pinned by SHA-256. Its 1,019 entries
have one `SFML-2.6.2` root, no absolute or parent-traversal path, no device or
FIFO entry, and 21 macOS framework symlinks whose targets all remain inside the
archive root. The RPM uses system FLAC, FreeType, OpenAL, Vorbis, X11, Xcursor,
Xrandr, OpenGL, and udev dependencies. Upstream still embeds the libraries it
does not support replacing in this release: glad, minimp3, stb_image, and
Vulkan headers. The License field accounts for those components and the
public-domain example assets in the source archive.

System, Window, Graphics, Audio, and Network all remain enabled. The complete
upstream test suite builds and runs four registered tests for System, Window,
Graphics, and Network; upstream 2.6.2 has no Audio test target. The installed
smoke test therefore also compiles a consumer through installed CMake metadata,
checks every pkg-config module, round-trips a PNG through Graphics, round-trips
a WAV through Audio, and validates Network packet serialization. It avoids
opening a display, audio device, or external network socket, so it is suitable
for the QEMU-user CI policy without weakening the packaged feature set.

Fresh fixed-repository metadata (`repomd.xml` SHA-256
`1e7269d6fa08e8f837e0ead13ad324e7f4ee5569dde6691378a61a806145bc14`)
confirms all direct BuildRequires as riscv64 packages and confirms that the
repository has no existing SFML package or capability provider. Network access
is permitted by CI, but this build consumes only the pre-fetched, verified
source and does not require network access during upstream build logic. RISC-V
status remains unknown until the pinned openEuler RVA23/QEMU workflow completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, smoke test, and documentation.
