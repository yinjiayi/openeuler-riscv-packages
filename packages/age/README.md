<!-- SPDX-License-Identifier: Apache-2.0 -->
# age

The 1.3.2 source-corrected CI built and installed the target RPM, then exposed
the smoke test's stale `v1.3.1` version literal. All four installed commands
are now checked by full-line match against `v` plus the installed RPM version.
The encryption/decryption round trip, inspection checks and original Go test
suite are unchanged. This correction is not a claim that the new head passed CI.

This directory packages the official `https://github.com/FiloSottile/age`
release `1.3.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The official
tag source archive is pinned by SHA-256 `b07c28c6c4bdafa272073a310b75bc22c49da8904585a89c30e5ca4233e63843`
in `sources.yaml`; the reviewed archive has one `age-1.3.2/` root and no
absolute paths, parent traversal, or symlinks.

The `v1.3.2` tag resolves to upstream commit
`b74dce4cdbe35b5e5f66c06d9612b72f89028758`. Source archive members were
matched to the complete official Git tree. The automated update incorrectly
selected `age-v1.3.2-darwin-amd64.tar.gz`; that executable distribution is
not a source archive and must not be used to build this RISC-V package.
The corrected archive retains all 14 upstream Go test source files.

The frozen discovery snapshot in `package.yaml` cross-checks Arch stable,
Debian stable, Fedora 44, openSUSE Tumbleweed, and Ubuntu. Those distribution
records are lineage evidence only: no distribution recipe or AUR `PKGBUILD`
was executed. The upstream BSD-3-Clause license is retained by the package;
Apache-2.0 covers only the original packaging metadata and tests in this
repository.

The SPEC builds the four commands from the source module (`age`, `age-keygen`,
`age-inspect`, and `age-plugin-batchpass`) with `CGO_ENABLED=0`, and installs
the four upstream man pages. CI may resolve the pinned Go module dependencies
over HTTPS during the build. `%check` runs upstream's complete `go test ./...`
suite and checks the version embedded in every command. Installed smoke then
generates an X25519 identity, encrypts and decrypts a local file, and inspects
the resulting age container without network access.

Upstream `go.mod` declares Go 1.25.0 and release toolchain Go 1.27.0; its
test dependencies and defaults are unchanged. This source-input correction
does not establish target toolchain/dependency availability or build/install
success. Fresh exact-head CI and physical RPM/SRPM acceptance are required.
