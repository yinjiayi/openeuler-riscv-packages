# QBE

This directory packages QBE 1.3 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23.

The frozen discovery snapshot cross-checks the canonical QBE component across
Arch stable Extra, Debian stable, Fedora, openSUSE Tumbleweed, and Ubuntu
26.04 LTS. No distribution packaging content was executed.

The official release index identifies 1.3 as the current stable release and
publishes its archive SHA-256 and source commit. The independently downloaded
archive matched that digest, has one `qbe-1.3/` root, contains no absolute or
parent paths, and carries the MIT license in `LICENSE`.

QBE 1.3 natively includes a `riscv64` backend. The RPM builds all upstream
backends, runs the complete upstream `check-rv64` suite in the locked QEMU
environment, and smoke-checks installed RISC-V assembly generation without
network access.
