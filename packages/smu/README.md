<!-- SPDX-License-Identifier: MIT -->
# smu

This directory packages upstream `https://github.com/Gottox/smu` version `1.5` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The canonical component is `github.com-gottox-smu`; its AUR discovery lineage
is retained only as discovery evidence. No distribution recipe was executed.
The official stable `v1.5` tag was checked against commit
`67be1bfcb8643531ce7063423a7e45a2225439b8`. `sources.yaml` fetches that fixed
commit archive with SHA-256
`7b2ddeeb4d58cf880f203aacdd6ecb3fadcd2f63c52a213662c3c574905ff511`.
All eight archive members were reviewed; the release LICENSE is MIT/X
Consortium, and no bundled image or separate third-party payload is shipped.
The upstream release has no published signature asset; the archive is not
misrepresented as signature-verified.

The recipe preserves the original `all` and `install` targets, CLI behavior,
`-Wall -Werror -ansi` compiler checks, library search path, and both original
`documentation` and `testdoc` files. Only compiler/link settings and installation
prefixes are set to distribution values. There is no source patch and no
upstream test target. The mandatory downstream QA executes both unchanged
fixtures in full via stdin and file entry points in default and `-n` modes,
checks exact markup/escaping/list/link/image text outputs, CLI error/version
contracts, spaced/dash-prefixed file names, and allocation-growth/UTF-8 input.
Literal image/link URLs are only parsed; tests do not fetch them. QA runs on the
built and staged executables in `%check` and on installed RPMs in the smoke
test. Installed manual, documentation and both license copies are verified.

`smu-tests` contains the required offline checks and fixtures. The original
`smu.h` is not backed by an installed library/API implementation, so no fake
development library is exposed. Build dependencies are supplied by the target
repositories before the unprivileged network-disabled build. The projected
namespace has no entity/name overlap; the existing filesystem ghost ancestor
of the debug path still requires real target installation evidence, not a
static waiver.

The default raw-HTML passthrough remains enabled. `-n` is tested as upstream
escaping behavior, not claimed to be a security sanitizer or complete Markdown
compatibility. Local work performed only static, source-verification and
repository-tooling checks: compilation, RPM build/install, QEMU and target
execution are reserved for hosted CI and must pass before merging.
