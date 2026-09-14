<!-- SPDX-License-Identifier: Apache-2.0 -->
# libsdl2-ttf

This directory packages the upstream `SDL2_ttf` 2.24.0 shared library and
development files for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. It supplies
the `SDL2_ttf` and `SDL2_ttf-devel` RPM names required by dependent packages,
including the inventory-tracked `xsystem35-sdl2` package.

The immutable discovery snapshot records Ubuntu 26.04 LTS `libsdl2-ttf`
2.24.0+dfsg-3 lineage. Upstream's latest SDL2-series tag is
`release-2.24.0` at commit `2a891473eaf05ba1707a4b7913e6c4db7de7458a`.
The official 13,335,900-byte release asset is pinned to SHA-256
`0b2bf1e7b6568adbdbc9bb924643f79d9dedafe061fa1ed687d1d9ac4e453bfd`.
Its 1,622 archive members share the `SDL2_ttf-2.24.0` root and contain no
absolute path, parent traversal, hard link, or special member. All five
symlinks resolve within that root. The detached signature names issuer
fingerprint `1528635D8053A57F77D1E08630A59377A7763BE6`; the committed SHA-256
remains the mandatory CI source identity and the signature is advisory.

The build explicitly disables vendored dependencies and sample programs, and
enables HarfBuzz shaping against the target repository's SDL2, FreeType, and
HarfBuzz development packages. `%check` initializes SDL and SDL_ttf, confirms
the linked 2.24.0 library, reads nonzero FreeType and HarfBuzz versions, and
renders text with the release archive's Roboto test font into an SDL surface.
The installed smoke test repeats that public-API check through the packaged
`SDL2_ttf.pc` metadata. The exact image-locked repository metadata has SHA-256
`1e7269d6fa08e8f837e0ead13ad324e7f4ee5569dde6691378a61a806145bc14`;
it resolves `SDL2-devel` 2.30.0, `freetype-devel` 2.13.2, and
`harfbuzz-devel` 8.3.0 for `riscv64`. RISC-V status remains unknown until the
pinned CI build and installed-RPM smoke test complete.

Exact-head Package CI run `34004026840` for commit
`ae23554395a982144d5e8a2e6f232dcb95f6d35a` completed the audited dependency
transaction and reached `rpmbuild`. Upstream CMake installed both development
linker names, but Release 1 omitted `/usr/lib64/libSDL2_ttf-2.0.so` from the
development file list, so RPM rejected the otherwise completed install as an
unpackaged file. Release 2 assigns that upstream-installed symlink to
`SDL2_ttf-devel`; source, build features, `%check`, and installed smoke coverage
remain unchanged. A fresh exact-head target build is still required.

External source files remain under upstream's Zlib license. Apache-2.0 covers
only this repository's original packaging metadata, tests, and documentation.
