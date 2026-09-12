# pigz

This directory packages pigz 2.8 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23.

The frozen discovery snapshot cross-checks the canonical component across
Arch stable Extra, an AUR metadata-only derivative, Debian stable, Fedora 44,
openSUSE Tumbleweed, and Ubuntu 26.04 LTS. No distribution recipe or AUR
content was executed.

The source is the immutable versioned archive linked by the official pigz
release page. That page independently publishes the same SHA-256 recorded in
`sources.yaml`. The archive has one `pigz-2.8/` root, no absolute or parent
paths, and carries the Zlib license text in `README` and `pigz.c`.

The RPM builds with the fixed openEuler toolchain and system zlib, retains the
complete upstream `make test` target, and performs a separate installed
round-trip smoke test. Network access is allowed only during source retrieval;
the build and tests are offline.
