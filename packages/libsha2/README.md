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

The bounded CI job budget is 240 minutes, within the existing 360-minute
schema limit. At head `3a122a6e47a0c723eeb53a81dc26077951929382`, Package CI
run `39162513169/1` exhausted its 3236-second remaining build allowance after
the complete original default driver had returned successfully and during
the staged shared-library replay (24 huge-case starts observed, last at
84 percent). Dependencies had installed successfully. This is evidence of
an insufficient job budget, not a source assertion failure or a complete
build. The longer bounded budget also reaches installation through the
separate shared infrastructure change #2708, merged as
`30365aea07de1f190f5876e480d908853893db98`; setup time is deducted and evidence
time is reserved. All16 huge cases and all default, staged and installed
shared/static replays remain unchanged. The replacement exact-head CI must
still prove that the full build and ordinary installation finish; increasing
a deadline does not itself establish success or authorize a blind rerun.

The original archive is shipped in the tests subpackage and checked by SHA-256
before replay; the installed header is compared to it and shared SONAME checked.
Upstream's hardcoded `/usr/lib` installation tree is moved intact within the
isolated RPM buildroot to openEuler's `/usr/lib64`. All API manual pages remain.

Target: openEuler 24.03 LTS SP3, riscv64, RVA23, repository-locked image.
No local source/RPM/QEMU run, native-hardware, timing or security assurance is
claimed. Repository tooling validation is not target build evidence.
