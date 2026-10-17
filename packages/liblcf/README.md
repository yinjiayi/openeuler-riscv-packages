# liblcf 0.8.1

Official EasyRPG/liblcf tag `0.8.1` is the unsigned annotated object
`016847fb32496c167eba6b2494e7f7867c87b339`, pointing to commit
`92c4450a1bc1acb58bd02bbb99b57e5036919cdf`. Its GitHub web-flow commit
signature was independently verified at the current time using the complete
official key, fingerprint `968479A1AFF927E37D1A566BB5690EEEBB952194`.
This is a GitHub signed release merge, not a personal maintainer signature or
an archive detached signature. All 336 archive files match their official Git
blobs, sizes and executable bits. Archive SHA-256:
`f16dd65f798bbd6e4e2eeb6411e69cdb1fb04c7bbf21e7a15e01bb373d41837b`.

Default shared-library/SONAME 0, INI, ICU, XML, both tools, MIME support and tests
are enabled unchanged. Benchmarks remain upstream-default OFF. Relative lib64
keeps CMake exports relocatable for staged and installed consumers. Normal
debug output is retained. No target feature is disabled for packaging.
The packaging RelWithDebInfo flags use RPM optflags followed by `-UNDEBUG`;
the installed-originals target also puts `-UNDEBUG` in target compile options.
This avoids claiming that an earlier global flag overrides a later `-DNDEBUG`.

`0001-defer-staged-mime-cache.patch` changes only DESTDIR cache refresh: the MIME
XML is installed normally, generated shared caches are refreshed on the real
installed filesystem by RPM post-transaction/removal scripts. Direct unstaged
upstream install still refreshes the cache. Remove when upstream provides an
equivalent packaging-aware integration. `0002-add-installed-checks.patch`
materializes the exact retained downstream QA files through the repository's
actual SPEC/source/patch staging contract; it does not change upstream code or
tests. Both patches are locally authored MIT, not claimed upstream-accepted.

`0003-find-inih-pkgconfig-module.patch` corrects the upstream finder request from
`libinih` to the supplied `inih` pkg-config module. The exact target inih-devel
62-1 RPM provides `inih.pc`, its `/usr/lib64` link-directory hint and a valid
`libinih.so` linker symlink. The original PR configure failed with
`INIH_LIBRARY` missing after the dependency transaction succeeded. An earlier
C++ ABI detection probe also failed; its cause is not established by the
retained log, and this small compatibility fix is not proof of target success.
The same finder is installed for downstream CMake consumers. Remove this
locally authored MIT patch when upstream uses the correct supplied module.
All original defaults, tests, tool and library code remain unchanged; the next
exact-head target build and installed consumers must validate the correction.

`%check` runs original `check` → `check_lcf` → `test_runner_lcf` (not CTest).
All ten original `.cpp` files and bundled doctest.h are installed unchanged and
recompiled against installed headers/shared library. Separate downstream
pkg-config and CMake consumers check INI, ICU encoding and LMU binary/XML
round-trips. Original CLI help statuses, LCF-to-XML conversion and string
extraction are checked offline. These are functional/package checks, not
performance, full format conformance, security or native-hardware claims.

The project is MIT; original INIReader carries the complete BSD-3-Clause notice.
Vendored span-lite is BSL-1.0; doctest is MIT and identifies copied Catch/lest
BSL code. Original notices and independently verified complete official Boost
and doctest texts are included as declared sources and installed licenses.
The preset generator and generated JSON declare Unlicense; those source-only
files remain intact in the SRPM and are not installed or executed here.
Downstream QA has a separate complete MIT notice. No fonts, game data or other
external assets are needed for the original suite.

Discovery aliases `easyrpg-player` and `liblcf-git` are retained as lineage, not
used to replace the actual official stable component/version. Full current
canonical/open-PR and target provider/namespace checks precede submission.
Provider inventory is not an observed DNF transaction. Local verification is
metadata/tooling/GNU patch `--fuzz=0`/source-only; no local upstream/RPM/QEMU
execution. Hosted riscv64 build/install/full original tests/smoke, physical
RPM/SRPM acceptance and final merge gates remain required.
