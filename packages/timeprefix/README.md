# Timeprefix

Timeprefix 3.1.2 prefixes input lines with boot-time and UTC text. The fixed
official source archive is SHA-256 verified and its complete ISC notice is
retained in the main and tests subpackages and in the unchanged QA/SRPM archive.

The original default build and complete `make check` pipeline remain unchanged.
Staged and installed checks repeat the exact original normalized-output MD5
pipeline and add payload preservation, empty/long input, `--` and usage checks.
These are functional formatting checks: they do not measure clock accuracy,
monotonicity, timing/performance, suspend behavior or leap-second correctness.
Those native clock properties require a suitable native RISC-V environment;
QEMU-user results cannot establish them. No clock/syscall branch is disabled.

No source patch or local source/RPM/QEMU execution. Exact-head required CI,
real target build, ordinary installation and physical RPM/SRPM acceptance remain
merge gates; static admission is not build or native-clock acceptance.
