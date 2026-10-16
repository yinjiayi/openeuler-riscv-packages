<!-- SPDX-License-Identifier: Apache-2.0 -->
# fastahack

This directory packages upstream `https://github.com/ekg/fastahack` version `1.0.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The canonical package is the upstream `fastahack` command, not a separately
installed library ABI. The default Makefile target and install rule are retained.
Official tag v1.0.0 resolves to bb332654766c2177d6ec07941fe43facf8483b1d;
the fixed archive SHA-256 is recorded in sources.yaml. All 20 regular upstream
files were compared to their Git blobs. No third-party packaging is executed.

The root MIT license covers the upstream code; bundled libdisorder has a complete
GPL-2.0-or-later license and copyright notices. Both full licenses and the
libdisorder source attributions are installed. The combined executable is
declared `MIT AND GPL-2.0-or-later`.

Upstream registers no automated check target; its CI runs the default `make`.
All five original FASTA fixtures are retained byte-for-byte. The downstream
contract means additional checks, not an upstream test-suite pass: three valid
fixtures are compared to an independent sequential parser for complete dumps
and indexed regions; two invalid fixtures must be rejected. It also checks
entropy, help, and three negative CLI paths. The same contract runs against
the build-tree, staged, and installed executables.

The two-line generic patch corrects LF line-boundary and CRLF byte offsets in
indexed subsequences. It does not suppress tests, change fixtures, or disable
features, and is not evidence of an architecture-specific defect. Its removal
condition is an upstream release containing the equivalent correction.

The 17 build requirements have providers in the configured target repository
metadata with no canonical-name/file collision observed. This is metadata
closure, not a dependency transaction or target execution result. Local checks
are trusted tooling tests, shell syntax, inert patch/oracle checks and source
verification only. Real RPM build/install and retained-fixture execution must
be established by exact-head target CI; native RISC-V performance is unclaimed.
