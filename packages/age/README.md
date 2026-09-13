<!-- SPDX-License-Identifier: Apache-2.0 -->
# age

This directory packages the official `https://github.com/FiloSottile/age`
release `1.3.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The GitHub
tag archive is pinned by SHA-256 `396007bc0bc53de253391493bda1252757ba63af1a19db86cfb60a35cb9d290a`
in `sources.yaml`; the reviewed archive has one `age-1.3.1/` root and no
absolute paths, parent traversal, or symlinks.

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
