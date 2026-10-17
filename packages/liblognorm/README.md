<!-- SPDX-License-Identifier: Apache-2.0 -->
# liblognorm

This directory packages liblognorm `2.1.0` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official immutable release asset is independently
SHA-256 pinned, agrees with its publisher attestation, and passed single-root,
path, link, and special-entry safety inspection. Committed snapshot
`discovery-20260808T165000Z-9a89920c269462cd` is the immutable source of the
manifest's `2026-08-08T16:50:00Z` lineage. It records AUR `2.0.9-1`, Debian
`2.0.6-5`, Fedora `2.0.6-17.fc44`, openSUSE `2.1.0-1.3`, and Ubuntu
`2.0.9-1`; its canonical component has no Arch stable row. Current official
2.1.0 release verification is a separate hard gate, not a rewritten snapshot
observation.

AUR was captured as RPC metadata only; no PKGBUILD or distribution spec was
executed. The offline build enables regular expressions, advanced statistics,
the command-line tools, the testbench, and the new TurboVM engine. On
`riscv64`, upstream's TurboVM uses its scalar backend instead of x86 SSE4.2 or
AArch64 NEON, while still running all TurboVM tests. The complete upstream
shell and C suite remains enabled. Installed smoke parses a rulebase through
both the classic and TurboVM paths and compiles a public API version probe.

The installed JSON assertion compares the complete parsed results from both
engines to exactly `{"name": "RVA23"}` and to each other. This avoids assuming
that classic and TurboVM use identical JSON whitespace: the official 2.1.0
TurboVM serializer writes compact key/value separators. Malformed JSON,
duplicate keys, extra fields or documents, unparsed input and wrong values
remain failures. Python's JSON standard library is already required by the
repository's installation harness; this adds no package runtime dependency.
This package-local assertion repair changes neither the upstream source nor
the complete default `%check` suite or enabled features. Replacement-head
target CI is still required to establish actual build and installed behavior.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
