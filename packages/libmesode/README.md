<!-- SPDX-License-Identifier: MIT -->
# libmesode

This directory packages official libmesode 0.10.1 for openEuler 24.03 LTS SP3, `riscv64`/RVA23. The official GitHub release is non-draft/non-prerelease and tag `0.10.1` resolves to `a3d894f2626bd2d97dfae03ca924782ce850294e`. The codeload archive has SHA-256 `c9dd90648e73d92b90f2b0ae41a75d8f469b116d3e6aa297c14cd57be937d99e`; `sources.yaml` deliberately gives those bytes the explicit `libmesode-0.10.1.tar.gz` cache filename used by SPEC Source0. Its root is `libmesode-0.10.1`.

The frozen Arch extra 0.10.1-3 rows for libmesode/libmesode-doc establish discovery lineage, not license authority or build proof. Libmesode is an independent fork of libstrophe with inherited `xmpp_` API names but distinct `libmesode`, `mesode.h` and `libmesode.pc` identities; it does not claim libstrophe filename or provider equivalence. The current canonical directories and all open PR file lists, and full official target primary/filelists metadata, were checked for the candidate's identity and installed paths. Provider closure is a static metadata projection, not a DNF solver or installation-success claim; supplemental namespace and actual products remain separate merge gates.

## Licenses and original notices

The MIT branch is selected where LICENSE.txt and source headers explicitly offer MIT or GPLv3. Original MIT, GPLv3 and root notices remain intact. The five MD5/SHA1 implementation/header/test members explicitly placed in the public domain are represented by `LicenseRef-Public-Domain`; this is not a claim that all project code is public domain. `src/snprintf.c`, `src/snprintf.h` and `tests/test_snprintf.c` carry Patrick Powell's 1995 permission to use for any purpose provided the notice remains intact on all source distributions, represented by `LicenseRef-Patrick-Powell`, not incorrectly relabelled MIT. All later attribution lines are preserved.

Before source patching and bootstrap/configure, SPEC copies all 83 original ordinary archive members byte-for-byte into a parallel `license-notices/` tree using `.notice` names and creates a SHA-256 manifest. The sole relative symlink `README` targets the same archive's ordinary `README.markdown`; it is not followed during the source audit or notice-copy loop. The original symlink and target remain in the unchanged source archive. The full notice tree is installed with `%license`, with every original-copy checksum verified in `%check` and installed smoke. Newly generated Autotools helpers retain their tool-provided notices; the 83-member inventory refers to original archive members, not an invented inventory of future generated output.

## Default build and checks

The upstream bootstrap operation is retained (`mkdir -p m4; autoreconf -i`, with `-f` to regenerate consistently). Plain configuration defaults are preserved: Expat parser, OpenSSL TLS, shared and static libraries, all seven default `noinst_PROGRAMS` examples, and all twelve original `TESTS`. The recipe explicitly enables both libraries and leaves TLS enabled; it does not substitute the dummy TLS implementation, disable checks, add c-ares or run network examples. Doxygen configuration is present upstream but is not part of the original default build/install.

`make check` runs the unchanged parser, SHA1, MD5, random, SCRAM, context, Base64, hash, JID, snprintf, string and resolver programs. The resolver test uses fixed DNS packet fixtures and malformed random packet bytes, not live DNS queries. The non-default socket test mentioning an external host is retained in source but is not added to or removed from the default test list. Exact aggregate assertions require twelve passes, zero skips/failures/errors; the seven example executables must also exist. Assertions remain enabled via `-UNDEBUG`.

Six supplemental deterministic API cases exercise XML namespace/entity parsing and malformed rejection; escaped XML wire roundtrip; independent deep copy and clone/refcount ownership; JID construction/splitting and missing-domain failure; binary Base64 including NUL/non-ASCII and invalid rejection; and the SHA1 `abc` known vector. These functional encoding/digest checks are not cryptographic-strength, TLS-handshake, certificate-policy, network interoperability, kernel, performance or production-security validation. They supplement, not replace, the twelve upstream programs.

The same driver is installed and run through an absolute path. Installed smoke clears loader override variables, retains and hashes the full raw `LD_DEBUG=bindings` trace even on driver failure, and requires six exact normal-symbol bindings from that driver to the same installed `libmesode.so.0.0.0` file. Same-file checks accept legitimate loader path aliases without relaxing symbol/caller identity. Driver source and original notices are independently checksum-checked; no preload/interposer is used.

## Evidence boundary

Preparation performs inert source/license/default/provider review and trusted repository metadata/tooling gates only. No upstream source compilation, tests, RPM build or QEMU execution occurs locally. Target build/check and installed RPM success must be established by real exact-head CI and physical artifacts. `network_during_build: false` states that this recipe needs no undeclared fetch; actual CI containers remain network-enabled and source caches are checksum-reverified. Repository tooling tests do not prove package build or installed API success.

Original packaging and supplemental driver code use MIT; external source retains the permissions described above. The downstream resolver patch is architecture-independent; new exact-head target CI and physical artifacts remain mandatory.

## Bounded DNS compression decoding

A static source review found that a compression self-pointer or cycle repeats the
recursive name decoder arguments. This is a parser-risk finding, not an observed
network crash, exploit or CVE. The downstream patch replaces recursion with
iteration and one per-name pointer budget derived from the message size, keeping
the first compressed pointer length and bounded label output. All original 83
member notices are copied before patching; no default test or feature is removed.

Six supplemental target-only case groups reject a self-cycle, two-node cycle,
long cycle and malformed encodings, while accepting a long acyclic chain and
legitimate compressed SRV names. The positive executable links the actual default
static library. A separately linked untouched original-source control counts
decoder entries for the fixed self-pointer and exits exactly 97 at entry 65,
before uncontrolled stack growth. Exact status files, output signatures and
source/binary/log SHA-256 values are checked; a crash, timeout or arbitrary
nonzero exit does not pass. These checks run only in target CI after the twelve
unchanged upstream checks and API driver. Their results are pending for this head
and do not prove network reachability or general DNS/security correctness.

Remove the patch only after an official source update provides equivalent bounded
decoding and both original default tests and these positive/negative controls
are re-established on the replacement exact head. The source archive and installed
API smoke remain unchanged.

The original-source control is compiled through a separate supplemental make
target that reads `CC` and `DEFS` from the same generated `Makefile` as the
default library. This preserves the actual configure feature decisions,
including the `snprintf`/`vsnprintf` wrappers, rather than supplying fake
compatibility functions or hard-coding a successful feature probe. The earlier
standalone command omitted those definitions and failed to link `xmpp_snprintf`;
that was a test-harness failure before either DNS control executed. The control
source, instrumentation, exact 97/0 status requirements, output hashes, twelve
original tests and installed API smoke remain unchanged. A corrected recipe
still requires replacement exact-head target CI; local tooling checks are not
proof that these target programs link or pass.
