<!-- SPDX-License-Identifier: Apache-2.0 -->
# unclutter-xfixes

This directory packages upstream `https://github.com/Airblader/unclutter-xfixes` version `1.6` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Source and compatibility

Canonical component: `github.com-airblader-unclutter-xfixes`. This is the
Xfixes rewrite, not the older original unclutter project. The executable and
manual keep their original `unclutter` names; full target primary and filelists
metadata were checked for both package-name and installed-path conflicts.

- Fixed official release: https://codeload.github.com/Airblader/unclutter-xfixes/tar.gz/refs/tags/v1.6
- Archive SHA-256: `6f7f248f16b7d4ec7cb144b6bc5a66bd49078130513a184f4dc16c498d457db9`.
- All 21 original release members were reviewed. The MIT license and original
  Ingo Bürk notice are retained; there are no source patches.
- The original `all` target, Xfixes/XInput2/libev dependencies, five-second idle
  default, CLI options and AsciiDoc-generated manual are retained. Packaging
  flags are supplied in the environment so upstream's added flags and libraries
  are not overridden. Only the installation license directory is adapted.

## Checks and evidence boundaries

Upstream supplies no test or check target. The downstream Python checker runs
identically against the staged installation in `%check` and the installed tests
subpackage. It verifies the fixed source archive, both license copies, CLI
version/help/error statuses, and five bounded private-Xvfb cases: original idle
default, start-hidden motion, allowed-button wakeup with a configured ignore
list, legacy idle/onescreen options, and explicit display selection. XTEST
supplies input and debug traces confirm hide/show lifecycle paths; bounded
repeated input accommodates upstream selecting XI2 events after its start-hidden
trace. No tests are skipped and no real user's X display is accessed.

These traces are not cursor-pixel visibility, physical-input, touch, native
display/hardware, security-isolation or performance proof. Xvfb is a downstream
functional check, not a native RISC-V runner. The tests RPM retains the original
archive and checker for reproducible installed checks.

Target dependencies were admitted against complete official and immutable
supplemental metadata, not a full target DNF solver. Local checks are limited to
repository validation, tooling tests, golden evaluation and source verify-only;
upstream code, RPM and QEMU are not run locally. Real exact-head target CI,
ordinary DNF installation, physical RPM/SRPM checks, current-main protection and
explicit squash remain required before merge. RISC-V status remains unknown
until that evidence exists.
