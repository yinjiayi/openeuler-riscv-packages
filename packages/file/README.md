<!-- SPDX-License-Identifier: Apache-2.0 -->
# file

This directory packages file `5.48` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The immutable official release archive is SHA-256 pinned and
passed single-root, path, link, and special-entry safety inspection. Arch
stable and openSUSE Tumbleweed confirm 5.48; Fedora 44 stable, Debian stable,
and Ubuntu 26.04 LTS GA were on 5.46, so this is an intentional official-stable
forward release. Fedora updates-testing was not used.

AUR was queried through RPC only. Its matching `file-git` row is both VCS-only
and older than 730 days, so it was excluded as a source; no PKGBUILD was read
or executed. Distribution specs were untrusted, read-only lineage evidence.
The build explicitly enables every supported compression backend available in
the fixed target repository. It disables optional libseccomp support because
QEMU linux-user does not implement guest seccomp setup and the existing target
package is likewise not linked to libseccomp. This removes no upstream test:
the complete `make check` remains enabled. Installed smoke exercises both the
CLI and public libmagic API without network access.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
