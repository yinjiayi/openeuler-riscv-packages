<!-- SPDX-License-Identifier: Apache-2.0 -->
# bmake

This directory packages bmake `20260714` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Bmake is the portable distribution of NetBSD make. Its date
version records the upstream import date rather than a semantic version.

The target build container may use network access to retrieve the declared
archive. Its committed SHA-256 is verified before `rpmbuild` starts; the
upstream build and test operations themselves do not require network access.

The immutable discovery snapshot records Arch stable `20260714-1` under the
canonical component `crufty.net-help-sjg-bmake.html`. The build input is the
official NetBSD-hosted release archive, independently downloaded and pinned by
SHA-256 in `sources.yaml`; no distribution recipe was executed.

The archive contains 982 regular files below the single `bmake` root and no
absolute paths, parent traversal, links, devices, or FIFOs. Its top-level
`LICENSE` calls the distribution BSD-3-Clause, while retained source notices
also include BSD-2-Clause and BSD-4-Clause-UC terms. The detached signature is
recorded as advisory because the archive checksum is the required build gate.

Upstream's `boot-strap` builds without an existing bmake and automatically runs
the unit suite. The SPEC also invokes the explicit test operation in `%check`.
The openEuler target repository supplies `ksh`, `tcsh`, and Lua so shell-specific
cases and `check-expect.lua` can run. RPM construction uses the repository's
fixed unprivileged build identity because upstream enables `objdir-writable`
only when the effective UID is nonzero. The local Darwin cross-check executed
all 398 tests enabled by upstream there and reported `All tests passed`; that
is host-portability evidence only, not an openEuler/RISC-V RPM result.

The noarch `mk-files` subpackage owns the portable `*.mk` collection and is
required by the bmake binary. This follows the upstream collection name and
the Fedora package convention; the target repository has no existing package
or provider with that name. The installed smoke test checks the package split,
version, compiled system-make path, compatibility links, variable expansion,
and a real dependency graph.

The packaging metadata and smoke test in this directory are Apache-2.0.
