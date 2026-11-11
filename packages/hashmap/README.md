# hashmap.c 0.9.0

Official `v0.9.0` resolves to `3735986914fc1c4e6a9123b406d0970666aa4aec`.
All six Git files and executable modes match the fixed archive, SHA-256
`45c51cd2abe266995b88bb9609551806cfaf69919579ea186942f7c4e0fae913`.
No upstream implementation or test source is patched.

Discovery is the [credited bundled component in Debian orbvis](https://sources.debian.org/src/orbvis/0.3.4-1/README.md),
not a standalone Debian package or a claim about the new target build.
Canonical package naming, aliases, capabilities and owned paths are screened
against all open PRs and the complete current target repositories before PR creation.

Preserve the documented `-DHASHMAP_TEST` default suite, including all 2000
elements and randomized allocation failures. `BENCH`, `N`, and `SEED` are
unset so inherited settings cannot switch to benchmarks or shrink the suite.
Assertions stay enabled. Benchmarks are not run; no timing, performance or
native-RISC-V claim is made.

Upstream has no installation build system. Install `hashmap.h` and
`libhashmap.a`; consumers link the archive. The test package retains the
unchanged source needed for the original self-contained suite. An additional
downstream consumer checks the installed archive/header, 2000 insert/get/delete
operations, iteration and all three hash helpers. The original suite is never
replaced by the consumer.

The root MIT grant and embedded notices remain intact. SipHash carries a CC0
dedication, xxHash a BSD-2-Clause notice. Complete pinned official SPDX v3.27.0
texts supplement those notices. Only the BSD copyright placeholders are filled
with the existing Yann Collet 2012–2021 attribution; no relicensing is asserted.
Real target build, installation and physical RPM/SRPM acceptance remain CI gates.
