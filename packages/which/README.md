<!-- SPDX-License-Identifier: Apache-2.0 -->
# which

This directory packages GNU Which `2.25` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Fedora 44, Arch stable, and openSUSE Tumbleweed independently
confirm the official 2.25 stable release. Debian stable and Ubuntu 26.04 LTS
GA do not package this upstream component: they provide the similarly named
command from `debianutils`. Those functional-provider snapshots are recorded
for cross-distribution review but are not treated as GNU Which version or
source evidence.

The immutable official GNU archive is pinned by SHA-256 and passed inspection
for a single expected root, safe paths and links, and no special entries. AUR
was queried through RPC only, and no AUR recipe was read or executed.
Distribution specs were reviewed only as untrusted, read-only lineage evidence
and were never executed. Upstream ships an Automake `check` target but no dedicated
test programs in this release, so the complete check target is retained and
the installed smoke test adds deterministic PATH ordering, `--all`, and
version behavior checks. All build and tests are network-free.

External source licenses remain those of the upstream project. The repository
license covers only original packaging metadata, scripts, and documentation.
