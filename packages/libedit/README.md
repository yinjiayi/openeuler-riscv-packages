<!-- SPDX-License-Identifier: Apache-2.0 -->
# libedit

This directory packages the official `20260512-3.1` libedit release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The upstream version is mapped to
RPM-safe `20260512.3.1`; the archive filename remains unchanged. It is pinned
by SHA-256 `432d5e7ea8b0116dd39f2eca7bc11d0eed77faa6b77ea526ace89907c23ea4a0`.
Its 99 members have one `libedit-20260512-3.1` root and no absolute path,
parent traversal, symlink, or hardlink. The official release page does not
publish a detached signature for this archive.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` freezes Arch core
`20260512_3.1-1`, Debian stable `3.1-20250104-1`, Fedora 44
`3.1-58.20251016cvs.fc44`, openSUSE Tumbleweed `20250104.3.1-1.5`, and Ubuntu
26.04 LTS `3.1-20251016-1`. No AUR row mapped to the official libedit
component. No PKGBUILD or Fedora spec was executed; Fedora dist-git was read
only to cross-check dependencies, file ownership, and the composite license.

The fixed target repodata contains every declared BuildRequires, including
`ncurses-devel` and `groff-base`. Upstream ships no test programs, so `%check`
retains and runs its complete recursive check target; the installed smoke test
then compiles, links, initializes, and closes a real EditLine object. No
downstream or RISC-V patch is currently required. RISC-V build status remains
`unknown` until the locked QEMU CI image runs the RPM build.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
