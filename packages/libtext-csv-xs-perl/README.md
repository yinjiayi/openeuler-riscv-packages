<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-csv-xs-perl

## Source-redistribution hold

`LicenseRef-Unresolved-Fixture` is a local evidence-gap marker for bundled
material whose redistribution provenance has not been established. It is not
a license grant, a declaration that permission is absent, or a finding of
infringement. The draft must not merge, publish, rebuild/upload target products,
or receive automatic updates while this conservative hold remains. Source
redistribution is marked disallowed pending review, not permanently forbidden.

The code's README, module POD, XS header and bundled `ppport.h` consistently
grant the same terms as Perl. That code grant does not by itself settle the
following archive-level observations:

- `t/70_rt.t` lines 527-531 contain five vehicle-review prose snippets from the
  RT #24386 sample, attributed to automotive publications and newspapers.
  Their review columns total 1,078 bytes and have no separately established
  redistribution provenance in this archive. Facts, short phrases and prose
  may require different treatment; this record makes no legal determination.
  The file is 29,547 bytes, SHA-256
  `4067570053bcab37853d9eedb3558b4d3910e612c82d2f6544f645f75e3b5715`.
- `LOVE_LETTER.md`, installed as documentation, reproduces Xan's document
  except for its trailing HTML comment. The bundled 6,190-byte file has SHA-256
  `1509820c465bc1f9b1977aa82dc3798b4d3474edc4c354f5404b9036245ed1c4`.
  Official [Xan source at immutable commit
  23d76437a73e273a0fcbbe7e389f1430d60c041d](https://github.com/medialab/xan/blob/23d76437a73e273a0fcbbe7e389f1430d60c041d/docs/LOVE_LETTER.md)
  has an `Unlicense OR MIT` project declaration. Its MIT grant explicitly
  includes associated documentation, with Andrew Gallant/Guillaume Plique
  copyright notice. The origin [LICENSE-MIT](https://github.com/medialab/xan/blob/23d76437a73e273a0fcbbe7e389f1430d60c041d/LICENSE-MIT)
  SHA-256 is `cefd1455331ba0ac84de92e921e28d5469e6feb9ce5479081851ef79ccc3a230`;
  [UNLICENSE](https://github.com/medialab/xan/blob/23d76437a73e273a0fcbbe7e389f1430d60c041d/UNLICENSE)
  SHA-256 is `b5065838cbac452dfc855ba6e6e031481ad2c68406f70d21ead9321374653e6c`.
  This is a fixable origin-notice/aggregate-license gap, not evidence that the
  original author withheld permission. It does not resolve the vehicle sample.

`SECURITY.md` is **not** a blocking item. The official
[CPANSec guide](https://security.metacpan.org/docs/guides/security-policy-for-authors.html)
explicitly permits policies based on its recommended wording and prior
versions under its public-domain/0BSD terms and says resulting policies may be
covered by the software's license. No source notice is removed or rewritten.

All source pins, original tests, wrapper regression and installed smoke remain
unchanged. Historical target CI for head `f2b10bf068873b181261e295e41e23d08aea88c9`
passed the 35-file/52,610-assertion suite and wrapper check; that is technical
evidence, not aggregate source-license clearance or current-head CI success.
After provenance review and notice repair, the hold must be explicitly lifted
and complete target CI rerun on the then-current exact head and main.

## Supplier scope and historical technical evidence

This is a deliberate newer-version supplier, not a package-missing claim.
The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains `perl-Text-CSV_XS` 1.48 for riscv64. The target's Text::CSV 2.04
wrapper requires XS at least 1.53 to select the XS backend. That mismatch
is the verified dependency cause of failed PR #2296; a successful build of
this separate supplier alone will not repair or publish #2296.

The frozen inventory records 1.61, while official stable CPAN is now 1.64.
The pinned 287,904-B `Text-CSV_XS-1.64.tgz` SHA-256
`65c5662d4fe8ef3039a1b32f641634d0aae6ab10eabbb24f740c75332f2caf30`
matches publisher `CHECKSUMS`. Its archive contains one safe root and only
regular files/directories. README and module POD grant the same terms as Perl
for code; the aggregate RPM expression additionally records the unresolved
fixture evidence above rather than treating the whole archive as cleared.

The SPEC keeps all 35 default upstream `t/*.t` files in `%check`, including
the memory-regression test, and installs the XS module plus its examples as
documentation. An additional build-time integration assertion requires the
official target Text::CSV 2.04 wrapper and verifies that its default preference
selects the newly built XS 1.64 backend and correctly parses a quoted record.
Text::CSV is a test dependency only. Its installed-RPM smoke verifies the module
provider,
version, quoted CSV parse and serialization. This is functional QEMU-user
coverage, not a native RISC-V, memory-performance or security claim.

Exact-head target CI must demonstrate this RPM upgrades the official 1.48
package, retains full tests, and passes installed smoke. #2296 additionally
needs the newer supplier publicly resolvable and then its own full PP/XS
test and installed-smoke run. PR artifacts do not provide public RPM/SRPM
repository links.
