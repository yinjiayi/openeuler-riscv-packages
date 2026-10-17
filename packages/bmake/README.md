<!-- SPDX-License-Identifier: Apache-2.0 -->
# bmake

This directory packages bmake `20260912-1` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Bmake is the portable distribution of NetBSD make. Its date
version records the upstream import date rather than a semantic version.

The target build container may use network access to retrieve the declared
archive. Its committed SHA-256 is verified before `rpmbuild` starts; the
upstream build and test operations themselves do not require network access.

The immutable discovery snapshot records the historical Arch stable
`20260714-1` under the canonical component `crufty.net-help-sjg-bmake.html`.
It is discovery lineage, not the current build version. The current input is
the official fixed NetBSD-hosted `bmake-20260912.tar.gz` release archive:
`https://ftp.netbsd.org/pub/NetBSD/misc/sjg/bmake-20260912.tar.gz`, pinned in
`sources.yaml` with SHA-256
`b6bd32964cbe451be2838822c9d200b7c7e76a2a5947c03feb71dc6bd72988bd`.
No distribution recipe is executed to obtain or build this input.

The retained license declaration is BSD-3-Clause AND BSD-2-Clause AND
BSD-4-Clause-UC; upstream notices and the archive's `LICENSE` are preserved.
The current source manifest has no verified signature record. Matching the
committed archive SHA-256 is the required source gate, not an asymmetric
signature or an attestation of the build machine.

The RPM release is the SPEC's `Release: 1%{?dist}` value. `package.yaml` also
records release `1`; its former release `2` was stale metadata, not a separate
SPEC build or a reason to relabel `20260912-1` products. This maintenance change
aligns metadata and documentation with the existing SPEC. It does not update
the source version, bump or downgrade the actual RPM release, or change the
build recipe, default tests, smoke test or patches.

Upstream's `boot-strap` builds without an existing bmake and automatically runs
the unit suite. The SPEC also invokes the explicit test operation in `%check`.
The openEuler target repository supplies `ksh`, `tcsh`, and Lua so shell-specific
cases and `check-expect.lua` can run. RPM construction uses the repository's
fixed unprivileged build identity because upstream enables `objdir-writable`
only when the effective UID is nonzero. The historical `20260714` Darwin
cross-check executed all 398 tests enabled by upstream there and reported
`All tests passed`; it is old host-portability evidence, not current-source or
openEuler/RISC-V RPM evidence. A current-head target conclusion requires that
head's successful build and installed-smoke records plus verified artifacts.

The noarch `mk-files` subpackage owns the portable `*.mk` collection and is
required at the matching version and RPM release by the bmake binary. This
follows the upstream collection name and the Fedora package convention. The
installed smoke test checks the package split,
version, compiled system-make path, compatibility links, variable expansion,
and a real dependency graph.

Existing supplemental repository products were inspected separately: the
`20260912-1` SRPM's SPEC and source archive match the committed inputs, and the
binary package contains a RISC-V ELF executable. Those checks concern existing
bytes; they do not establish current-head CI, native RISC-V acceptance,
trusted-fleet recovery or a new public release. No local target build or
execution is required for this metadata/documentation reconciliation.

The packaging metadata and smoke test in this directory are Apache-2.0.
