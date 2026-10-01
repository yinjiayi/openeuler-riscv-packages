# tinycdb

This directory packages tinycdb 0.81 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23.

The frozen discovery snapshot cross-checks the canonical component across
Arch stable Extra, Debian stable, Fedora 44, and Ubuntu 26.04 LTS. No
distribution packaging content was executed.

The official project page identifies 0.81 as the latest release and links its
versioned archive. Independent retrieval produced the SHA-256 recorded in
`sources.yaml`; archive inspection found one `tinycdb-0.81/` root, no unsafe
paths, and an MIT `LICENSE` file.

The RPM builds the command, static and shared libraries, retains both upstream
static and shared test routes, and performs an installed constant-database
round-trip smoke test. All build and test phases are offline.
