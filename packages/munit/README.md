# Munit 0.2.0

The source-distributed C test framework from `nemequ/munit`, fixed at tag
`v0.2.0`, commit `ad67a3a2ca6b0e106c9c8d515772359eadcefad6`.
SHA-256: `74e14890607cf6f7dfe75df95bc66cab73db18dae4558ce7933392146fa29cb9`.
All 11 upstream files, including executable modes, match the fixed archive.
The complete upstream MIT `COPYING` is retained; no signature claim is made.

Discovery is the vendored `test/munit` component of Debian Chiaki 2.2.0-1.2,
whose `.gitmodules` names the official repository. This does not claim that
Debian packages standalone Munit, or that its vendored revision equals 0.2.0.

`munit` installs `munit.h` and `munit.c` for consumers to compile together,
following upstream's source-distribution model. `munit-tests` installs the
unchanged example, Makefile and license; neither package installs an ELF.
The build retains C99/debug defaults and the original `make test` contract.
Two ordinary cases and all nine parameter combinations must pass, with no
skips, in the original build tree, against staged installed sources, and again
after normal DNF installation. Forking and all default framework features stay
enabled. Only functional results are accepted; printed timing is not native
performance evidence. Windows/MSVC and historical compiler CI matrix coverage
are not claimed for this openEuler target.

Local validation is metadata, trusted repository tests, golden materialization,
fixed-source verification and static namespace/dependency screening only.
Target RPM build, default tests, all-binary DNF install, installed replay and
physical RPM/SRPM acceptance must pass on the exact PR head before merge.
