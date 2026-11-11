# Qrcodegen 1.8.0: original C and C++ ports

Debian trixie source `qr-code-generator` 1.8.0-1.2 is discovery lineage,
not a target build or redistribution-checksum substitute. The official v1.8.0
annotated tag resolves to `720f62bddb7226106071d4728c292cb1df519ceb`.
The fixed archive SHA-256 is
`d80795686f3e58448c7b76830bb5c40847b7eaae1996c28f0422a029b66c2bb0`;
all 52 original Git files and modes were checked. MIT notices remain intact.

The recipe preserves both original unmodified Makefile `all` targets and the
complete C internal suite (20 runner groups, original time-seeded randomized
loops, assertions enabled). Its private-symbol test requires the original
`QRCODEGEN_TEST` instrumented implementation. It is not represented as testing
the installed normal static archive. No cases or core features are disabled.

Staged and installed checks compile the entire unchanged C and C++ demos
against the actual public headers and static archives, then compare their
deterministic output with the corresponding original build demo output.
These are public-API consistency checks, not an independent QR decoder or
replacement for the complete original internal suite. Java, Python, Rust and
TypeScript ports are separate implementations and are outside this recipe.

Target build, ordinary all-binary DNF install and physical RPM/SRPM acceptance
remain CI gates. No local upstream compilation, RPM or QEMU execution occurs.
