# nettle

This directory packages Nettle 4.0 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23.

The frozen discovery snapshot cross-checks the canonical component across
Arch stable Core, AUR metadata-only derivatives, Debian stable, Fedora 44,
and openSUSE Tumbleweed. No distribution or AUR recipe was executed.

The source is the immutable versioned archive from GNU's official Nettle
directory. Independent retrieval produced the SHA-256 recorded in
`sources.yaml`; archive inspection found one `nettle-4.0/` root, no unsafe
paths, and the upstream GPL and LGPL license texts.

The RPM builds shared Nettle and Hogweed libraries against the system GMP,
runs the complete upstream cryptographic test suite, and verifies an installed
SHA-256 command result. The target build container has network access and may
retrieve the declared HTTPS source during the build; the committed SHA-256 is
verified before `rpmbuild` starts.
