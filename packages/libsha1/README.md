# Libsha1 1.1.6

Official Codeberg tag archive SHA-256
`55536baac47e1cc62ed33d87bbe1ffa42a96871c2d4e6c06ff81b7dc072d9318`.
Retain all original files and ISC copyright/permission notice. Frozen AUR
1.1.6-1 is discovery lineage; no PKGBUILD is executed.

Select upstream's existing config-portable.mk on RISC-V; the upstream default
x86 configuration deliberately requires x86 intrinsics. Build the complete
default all target (static, shared and test driver), preserve original
make check with no arguments, and retain all four huge-message cases.
Staged and installed checks compile unchanged test.c against each installed
shared/static library and run it without arguments as well. No skip-huge,
filter, assertion removal, changed expected digest or source patch.
Test duration for this complete suite must be established by target CI;
do not infer it from local inspection or replace it with a reduced smoke.

Upstream install hardcodes /usr/lib. Relocate that complete staged directory
to openEuler riscv64 /usr/lib64, retaining all libraries and symlinks; keep
all manual pages, installed header, source archive and original test driver.
Shared linkage must resolve libsha1.so.1 and installed header must match.
This legacy-algorithm package makes no security, performance or native-hardware
claim. No local upstream source, RPM or QEMU execution was performed.
Target CI and physical RPM/SRPM/install acceptance remain mandatory.
