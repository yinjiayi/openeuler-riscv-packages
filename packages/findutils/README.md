# findutils

This package tracks GNU findutils 4.11.0 for openEuler 24.03 LTS SP3 on
RVA23 riscv64. The official GNU archive is SHA-256 pinned, Epoch 2 and the
`findutils-help` split preserve target EVR and layout, SELinux support is
retained, and the complete upstream check suite is run serially. The upstream
locate implementation is built and tested but omitted from the payload because
target `mlocate` owns those paths.

The fixed RISC-V ABI uses unsigned plain `char`, while the C locale can expose
unavailable monetary fields with the signed-character `SCHAR_MAX` sentinel.
The build selects a package-owned gnulib `localeconv` replacement that
normalizes that representation to the standard `CHAR_MAX` interface. The full
upstream test suite remains enabled; no locale test is skipped or weakened.
