<!-- SPDX-License-Identifier: Apache-2.0 -->
# libecoli 0.11.8

Official stable `rjarry/libecoli` annotated tag `v0.11.8`
(`d8537bd5b4a9fa896ebeefa428514e05159c73cb`) commits source
`642e5a5c7224894a72ede66608a72e6fea2de39a`. The immutable official archive SHA-256
is `9c2fc12f056a6304d68291e9e8976f6e0d10f5049b4f87cecee5900d0aad5b4f`.
All 179 Git blobs match the archive, including one safe relative AI-document
symlink (not an instruction/build input). No source patch is applied.

The available annotated-tag PGP signature passed GnuPG 2.4.9 using the official
checked-in key independently matched to the publisher's GitHub account key.
Signing subkey: `D8B6A9907C3AB720428B606862718E0D666FC335`;
exit 0, GOODSIG/VALIDSIG, no expiry/revocation errors. GitHub reports `bad_email`
for its tagger-email check; no GitHub verified badge or Web-of-Trust certification
is claimed. The signed payload commits the exact source above.

Discovery lineage remains Fedora `0.10.1-2.fc44` from snapshot
`discovery-20260808T165000Z-9a89920c269462cd`; current official stable source was
independently rechecked without executing external distribution packaging.

License: BSD-3-Clause plus the explicit Austin Appleby public-domain dedication
in `include/ecoli/murmurhash.h` (`LicenseRef-Public-Domain`). Full BSD terms,
that original notice and all C/H copyright lines are installed; original test
sources and installed headers retain their notices.

The build preserves the standalone default shared library, assertions, C99,
werror, YAML/editline, all five examples and original HTML/man docs. All auto
features are enabled as in upstream CI; no wrap/network build access is allowed.
Target dependencies include libedit, libyaml, readline, Doxygen/doxygen2man,
libxml2, Graphviz, clang and Python. Full official/supplemental primary/filelists
joins found no package/capability/installed-namespace collisions; actual version
bounds still require target DNF/CI acceptance, not a claimed local solver result.

Upstream only installs the parse-yaml shell entry point. The recipe additionally
installs its unchanged built binary and original shell library to complete that
entry point's documented installation; other four unchanged examples are in
`/usr/libexec/libecoli`. Interactive sessions are not run automatically.

`%check` retains all 33 original Meson unit programs (including YAML), requires
33 OK/zero skips, and runs original `make check-symbols`. Installed smoke hashes
retained inputs, rebuilds/runs the same 33 programs against installed headers
and shared library, links the public symbols discovered by the original clang
AST generator, checks an independent exact-match/non-match parsing consumer,
and verifies `john`/`mike` completion with the original offline YAML fixture.
Installed headers are copied to a private path because the original generator
excludes `/usr` system headers; an empty symbol set cannot pass.

The diagnostic target run passed the 33 original Meson programs, the original
symbol-link check, all 33 downstream original units, the independent parsing
consumer, and downstream symbol generation/link/execution. It then failed at
our added output-count comparison: 269 `ec_` references were counted, but the
artifact did not retain the generated array or pointer output, so its complete
reference and line counts are not known.

The unchanged original generator emits every project-header function and
external-variable reference, not only names beginning `ec_`. The downstream
oracle therefore validates the complete emitted array, retains the independent
positive `ec_` count, and requires exactly one non-null pointer output per
reference. It rejects malformed/duplicate references and missing/extra/malformed
output. It prints all three integer counts before count comparison, including on failure,
for the next real target acceptance. This
also removes dependence on external `wc` text formatting. The precise failed
run cardinality remains unavailable; no target success is inferred from the
synthetic predicate fixtures. All original units, feature defaults, generator,
link/run, consumer and CLI assertions remain intact.

No local upstream/RPM/QEMU build was run. Metadata/trusted tooling/source-only
checks precede submission. Real target build/install/smoke, physical RPM/SRPM
acceptance and merge remain separate hosted-CI gates. This is userspace
correctness coverage, not native RISC-V or performance evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
