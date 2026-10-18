# libsha2

Portable bit-oriented SHA-2 library, including SHA-224/256/384/512,
SHA-512/224 and SHA-512/256, HMAC and state serialization.

The frozen AUR discovery lineage identifies upstream Codeberg libsha2 1.1.5.
It is discovery evidence, not executable packaging input. The official fixed
archive SHA-256 is `7924ff2d6ac6ac3e8e8845db0c986b03cc7cad53a026cf382a0a15218d9daca1`.
The complete ISC license and source copyright notices are retained. No source
patches are applied.

RISC-V uses the upstream-provided `config-portable.mk`, not the default
x86 intrinsic configuration. The original `all` builds static/shared libraries
and its test driver. `%check` runs the original `make check` without arguments,
with empty `CHECK_PREFIX` and `CHECK_FLAGS`: all16 huge-message cases remain,
as do both SHA-256 and SHA-512 test families, bit tests, serialization, HMAC
and file-descriptor checks. Additional staged and installed tests compile the
same original driver against each static/shared library and execute it without
arguments. These full replays may take longer under QEMU; CI runtime and real
build/install acceptance are still required, not inferred from validation.

The original archive is shipped in the tests subpackage and checked by SHA-256
before replay; the installed header is compared to it and shared SONAME checked.
Upstream's hardcoded `/usr/lib` installation tree is moved intact within the
isolated RPM buildroot to openEuler's `/usr/lib64`. All API manual pages remain.

Target: openEuler 24.03 LTS SP3, riscv64, RVA23, repository-locked image.
No local source/RPM/QEMU run, native-hardware, timing or security assurance is
claimed. Repository tooling validation is not target build evidence.
