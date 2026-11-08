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
backends. The recipe retains the complete upstream `check-rv64` suite in
the locked QEMU-user environment and the installed RISC-V assembly-generation
smoke check without network access. These are required validation routes,
not a claim that this repaired package has already passed them.

## Native-target test harness compatibility

Package run `39552897803/1` at failed head
`7194bd1ff990a40496b86545424bac31e20ae3be` compiled QBE and completed
RPM staging (`%install`), then failed in `%check`:
`Cannot find riscv64 compiler or qemu.` Install-smoke was skipped. The original
QBE 1.3 RV64 harness probes only cross-prefixed compiler names, although
the target container already has a native RISC-V GCC.

`patches/0001-test-native-rv64-compiler.patch` applies only to the fixed QBE
1.3 archive whose SHA-256 is
`d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320`.
On `uname -m = riscv64`, it first discovers the explicitly supplied native
compiler through upstream's existing compiler/runner function and uses the
native Linux test-driver pthread link flag. Other hosts retain the original
cross-compiler fallback. The original `check-rv64` target, explicit RV64
backend selection, every test case and upstream conditional skip policy
remain unchanged. No test result is suppressed or converted to success.

This package-local compatibility patch has not been submitted upstream;
no upstream write was made. Remove it when upstream `check-rv64` discovers
the native compiler. "Native" here describes target-architecture processes
inside QEMU user mode, not execution on native RISC-V hardware. The new
head's target CI must still establish build, full-suite and install results.
