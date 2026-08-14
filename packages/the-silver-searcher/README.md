<!-- SPDX-License-Identifier: Apache-2.0 -->
# The Silver Searcher

This directory packages the official The Silver Searcher 2.2.0 tag for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. CI downloads the official tag
archive over HTTPS and verifies its pinned SHA-256 before the network-enabled
target build.

The RPM installs the `ag` command, manual page, and Bash and Zsh completion
data with PCRE, LZMA, and zlib support enabled. Upstream's extended suite uses
the unavailable `python3-cram` package; `%check` therefore runs deterministic
file and standard-input searches directly with the just-built binary. The
installed-RPM smoke test repeats file-type and parallel-search coverage.

Release 2 backports upstream commit `21eaa1c4160b868b0c5bbf59da17974429f30055`,
which was accepted through upstream pull request 1377. It gives each global
symbol a single definition so the stable 2.2.0 source links with modern GCC's
`-fno-common` default; the patch is removed after a stable release contains
upstream merge commit `3f6ecb6c02f147d5d180b9d85373e74c83f675ec`.

The upstream command is Apache-2.0 and its bundled uthash header is
BSD-1-Clause. The repository license covers only original packaging metadata,
scripts, and documentation.
