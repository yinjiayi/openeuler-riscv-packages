# Lemonbar 1.5

Canonical upstream component: `github.com-lemonboy-bar`. Official stable v1.5
tag resolves to immutable commit `5420c86be097819028a9504c1cb6a8f7f23ab5c8`.
Source https://codeload.github.com/LemonBoy/bar/tar.gz/5420c86be097819028a9504c1cb6a8f7f23ab5c8
SHA-256 `8e364cfaf3de7430cd5f1e2d51fab7f0ec74abee1df73ffc901985152f9b74d3`.
Fresh discovery: AUR lemonbar1.5-2 metadata, official upstream URL,
https://aur.archlinux.org/rpc/v5/info?arg[]=lemonbar . No AUR recipe is executed;
no membership in the older frozen discovery catalog is claimed.

All eight original members were read. Retain upstream global MIT LICENSE and
all existing source attribution, including the original wmdia function reference.
No source patch, vendored binary, external font or image is introduced. Original
default all and install/doc/pod2man targets are retained with original appended
compiler flags and all XCB libraries. Official v1.5 has Makefile VERSION=1.4;
this internal help/man version is intentionally preserved, not silently rewritten.
RPM version follows the independently verified official v1.5 release tag.
Upstream has no test target. Its supplementary CI WITH_XINERAMA=1 build is also
compiled in an isolated copy, checked through private Xinerama with RandR disabled;
the original default RandR binary is the one installed, unchanged in feature choice.

Mandatory built/staged/installed downstream QA uses its own bounded Xvfb, fixed
font and independent ctypes-Xlib client. It checks exact no-DISPLAY failure (even
help connects first), original help/version semantics, invalid geometry, real
top/bottom geometry and WM_NAME/WM_CLASS/EWMH struts, actual formatted background
and underline pixels, clickable-offset output, default EOF cleanup and persistent
event responsiveness after EOF followed by graceful termination. No display is
borrowed; no shell command printed by a click is executed; no optional skip.
Default and supplementary build configurations each receive the same semantics,
not a compile-only success claim. Original notice/docs hashes and generated man
version are checked on installed RPMs; tests require exact base EVR.

Target: locked openEuler24.03 LTS SP3 riscv64 RVA23 QEMU-user, offline build,
unprivileged rpmbuild. No local upstream/compiler/target/RPM/QEMU execution.
Tooling tests and inert review are not target runtime, physical RPM/SRPM, native
or publication acceptance. Complete exact-head CI and real build/install/products
with full dependency/path verification still gate explicit protected squash.
No auto-merge is enabled.
