# Sxhkd 0.6.3

Canonical upstream component: `github.com-baskerville-sxhkd`. The official stable
0.6.3 tag resolves to immutable commit `2cc7aca40f38cd47fbeea1f37fe310ef34386435`.
Source https://codeload.github.com/baskerville/sxhkd/tar.gz/2cc7aca40f38cd47fbeea1f37fe310ef34386435
SHA-256 `ad02c39f0e72fe69616d9b7d652b3573b51d8a2b75543c2d516ceb16a4f0322c`.
Current Arch extra sxhkd0.6.3-1 metadata supplied the independent distro lineage:
https://archlinux.org/packages/search/json/?name=sxhkd . No external recipe was
executed and no membership in an older frozen discovery catalog is claimed.

All 28 original members, including the complete literal keysym table, were read.
Retain the global and source-file BSD-2-Clause notices, original documentation and
examples. No source patch, binary or added external asset. The original default
all target, object dependencies, CPPFLAGS, appended C99/pedantic/warning flags,
three XCB libraries and ordinary install remain unchanged. VERCMD=false selects
the original cat VERSION fallback for the pinned source archive, avoiding Git
metadata inherited from an unrelated outer checkout. Original prebuilt manpage
and examples are installed unchanged; doc regeneration and systemd service are
not part of original install. No upstream test target or suite exists.

Mandatory downstream QA runs against built, staged and actually installed binaries.
It creates its own bounded Xvfb with mandatory real XTEST input and an independent
ctypes-Xlib client. It checks exact offline CLI/version/display failure, actual
key and mouse grabs, press/release/control/brace expansion/chained chords, default
XDG/explicit/extra configuration, selected shell and exact daemon PID in real
command output, redirection/status FIFO, signal-driven reload/toggle and clean
termination. Readiness is proved through passive-grab ownership, not guessed sleep;
event completion is bounded and confirmed through commands and FIFO status.
No user display is borrowed and no original example is executed. A separate
file is used for each -r process because original -r does not promise truncation.
Installed LICENSE/README/manpage and every example are checked by exact original
SHA-256; the tests subpackage requires exactly the base package EVR.

Target: locked openEuler24.03 LTS SP3 riscv64 RVA23 QEMU-user, offline build,
unprivileged rpmbuild. No local upstream/compiler/target/RPM/QEMU execution.
Inert review and tooling tests are not target runtime or physical product acceptance.
Full exact-head CI, real build/install and actual RPM/SRPM/dependency/path evidence
still gate a protected explicit squash. No auto-merge is enabled.
