<!-- SPDX-License-Identifier: MIT -->
# tabbed

Packages the official [tabbed 0.9 release](https://tools.suckless.org/tabbed/) for openEuler 24.03 LTS SP3, riscv64/RVA23. Canonical identity `tools.suckless.org-tabbed` retains AUR/Fedora discovery lineage; no distro recipe is executed.

Fixed archive: `https://dl.suckless.org/tools/tabbed-0.9.tar.gz`, SHA-256 `0acf87457b7419e66fbfa3a9cec95ffb46d254c6b88b5e4bb7cc18c3a92008a8`. All nine original members are reviewed. Original MIT LICENSE and arg.h notice are retained in each RPM. No patch is required.

Original make all/install remain mandatory, building and installing both tabbed and xembed, two manuals and README. RPM supplies system flags and /usr paths; original preprocessor definitions, linked libraries, configuration and key bindings are unchanged. README's stale config.mk reference does not create a fictitious file. Ctrl-grave's original xwininfo/grep/sed/xargs/dmenu/xprop pipeline has explicit runtime file dependencies. Upstream has no test/check target, so none is skipped.

Mandatory staged and installed downstream QA verifies original archive/notices/docs/manuals, version/CLI errors/unavailable display, xembed no-environment/no-controlling-tty/foreground-and-background private PTY/exec-error branches, isolated Xvfb child parenting/dimensions/focus/titles/rotation/reordering/numeric-last-property selection/WM_DELETE/final-client exit, and default spawn plus -r replacement with exact XEMBED and argument lifecycle. Valid queued XEMBED messages are explicitly consumed before requiring WM_DELETE. Fixtures use bounded waits and finally cleanup, no public display or network server.

Local validation is source/static/repository tooling only; no compiler, upstream program, target binary, RPM or QEMU is executed locally. Exact-head CI must establish real target build/install. Physical RPM/SRPM and full provider/file-namespace acceptance remain separate. Private Xvfb does not prove native graphics hardware, compositor interoperability, timing, performance or security.
