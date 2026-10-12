<!-- SPDX-License-Identifier: Apache-2.0 -->
# xcb-imdkit

This directory packages upstream `xcb-imdkit` 1.0.9 for openEuler 24.03 LTS
SP3 on `riscv64`/RVA23. xcb-imdkit is an asynchronous implementation of the X
Input Method (XIM) client and server protocol using XCB; this package supplies
the runtime library and development metadata needed by the fcitx5 dependency
chain.

The frozen discovery snapshot is
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks xcb-imdkit
1.0.9 in Arch Extra, Debian stable, Fedora 44, openSUSE Tumbleweed, and Ubuntu
Resolute, and retains the `xcb-imdkit-git` AUR entry only as VCS metadata. No
distribution recipe or AUR content was executed.

The source is the archive of the publisher's annotated `1.0.9` GitHub tag,
which points to commit `44f5c8219bcae9e6afc2391dc50486efcf0bdf06`. The
archive is pinned by SHA-256 in `sources.yaml`. GitHub reports that the
annotated tag signature is valid, but the generated archive has no detached
signature, so checksum verification remains the build's cryptographic source
gate.

The package uses system libxcb, xcb-util, xcb-util-keysyms, and uthash rather
than the bundled uthash header. The fixed openEuler repository identified by
`ci/image.lock` contains every declared BuildRequires and contains no existing
`xcb-imdkit`, `pkgconfig(xcb-imdkit)`, or `cmake(XCBImdkit)` provider.

Upstream registers one display-independent CTest: a multilingual UTF-8 to X11
compound-text round trip. The interactive client and server demos are still
compiled, which checks their APIs and XCB/keysyms link closure, but upstream
does not register them as unattended tests because they require a live X
server. The installed smoke test verifies the RPM and pkg-config provider,
checks the installed header and CMake configuration, and compiles and runs a
separate multilingual conversion consumer against the installed package.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, script, and
documentation in this directory.
