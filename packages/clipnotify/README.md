# Clipnotify 1.0.2

Canonical component: `github.com-cdown-clipnotify`. Official stable 1.0.2 tag
resolves to immutable commit `22f7cb09d0b99af0aae7109aaff73760ef2dd5e3`:
https://codeload.github.com/cdown/clipnotify/tar.gz/22f7cb09d0b99af0aae7109aaff73760ef2dd5e3
SHA-256 `651b273b8a9b7ff0ec264741aceb6946c5732d716df484a5e0aa7e6629cdeb58`.
Fresh distribution discovery is official Arch extra clipnotify 1.0.2-3:
https://archlinux.org/packages/search/json/?name=clipnotify
No old frozen-catalog membership or AUR entry is invented.

All four original members were read. The exact upstream LICENSE dedicates this
software to the public domain and explicitly permits copying, modification,
publication, use, compilation, sale and distribution of source or binary for
commercial and non-commercial purposes. Retain this exact abridged notice as
`LicenseRef-clipnotify-public-domain`; it is not the full SPDX Unlicense or CC0.
No patch, embedded library or image. Preserve original default all, caller
compiler/linker flags, BSD search paths and X11/Xfixes libraries. Upstream has
no test/check/install target or manpage; package installation is explicit.

Mandatory downstream QA runs built and staged in %check and installed in the
committed smoke: exact no-DISPLAY status/error; one private bounded Xvfb with
XFIXES required; independent Xlib windows/atoms and verified ownership; fresh
original process for each PRIMARY and CLIPBOARD change, bounded alternating
ownership events to avoid startup subscription races, exact exit0/empty output,
cleanup. No optional skip, invented version flag or clipboard-content claim.
Installed original LICENSE/README hashes are checked. Tests subpackage requires
the exact base EVR, Python, X11, Xfixes, Xvfb and Bash. No display is borrowed.

Target is locked openEuler24.03 LTS SP3 riscv64 RVA23 QEMU-user; build is offline
and unprivileged. No local upstream/compiler/target/RPM/QEMU execution occurs.
Repository tooling and inert source/QA reviews are not target build/install or
native acceptance. Exact-head complete CI, real target build/install, physical
RPM/SRPM and complete namespace verification remain mandatory before protected
explicit squash. No auto-merge is enabled.
