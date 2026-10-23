# csvprintf 1.3.4

csvprintf is the official Archie Cobbs CSV formatter component, including its
`xml2csv` XSLT companion. This recipe targets openEuler 24.03 LTS SP3, riscv64,
RVA23. Target compilation, original tests, installed-RPM QA and physical products
must be established by exact-head CI; local metadata checks are not build proof.

## Fixed upstream source and license

Official repository: <https://github.com/archiecobbs/csvprintf>. Stable annotated
tag `1.3.4` resolves to tag object
`a45e5198df2a5cb0fc62e1b2b1b77f6feeef9ac1`, commit
`edbe73df5becf886eda45ad45866ca8d7433505e`, tree
`653b8f4f0c1a126e9a368f3ddf0c96d7b9e4a422`. The fixed official archive is
26,458 bytes, SHA-256
`9457761c003dcbae79cc3a01761992dc1423902a92025ed90a6ad81b93897d45`.
All 100 regular members match the official Git blobs. The exact tag/commit are
unsigned; `signature: null` is not a signature-verification claim. SHA-256 is
mandatory. No distribution recipe was executed or borrowed.

`COPYING` is Apache-2.0, SHA-256
`cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.
Preserve source, fixture and generated Autotools helper notices. Discovery is
the frozen openSUSE row `csvprintf` / `csvprintf` / `1.3.4-1.4` in snapshot
`discovery-20260808T165000Z-9a89920c269462cd`; its raw-row SHA-256 is
`0894d6450c28ce0264027115925e727da83d283d6a88a82b9f695053dbc9417f`.
The obsolete Google Code/AUR alias is discovery lineage, not this source.

## Retained build behavior

The Git snapshot lacks generated Autotools files and `gitrev.c`. The recipe
runs the original `autogen.sh`, whose cleanup removes `gitrev.c`, then creates
the release-generated declaration
`const char *const csvprintf_version = "1.3.4";` plus a newline. That matches
the exact release tag without invoking Git in an enclosing packaging checkout.
The upstream no-prerequisite rule does not replace the existing generated file.
This deterministic release completion is not a RISC-V source patch.

XML, JSON, Bash output, iconv, external printf, required xsltproc, optimization,
assertion, gprof and Werror defaults are unchanged. The recipe retains both
binaries, both man aliases, the XSL and all default documentation. No feature
or original test is disabled. There are no source patches.

## Original tests and installed QA

`%check` invokes the original `make tests` target and unchanged runners. Its
83 static slots mean 9 inputs times 8 comparisons plus 11 shell cases, not
83 observed passes. All 85 original test members and their expected bytes are
retained. Before invoking the target, the recipe fails closed unless `/bin/sh`
supports `pipefail`; it does not bypass a failing runner.

The selected official Bash 5.2.15 RPM header owns `/usr/bin/sh -> bash`, and
the official filesystem RPM header owns `/bin -> usr/bin`. Both RPM bytes are
SHA-256-bound to fresh official metadata. This addresses the dash incompatibility
risk statically; actual locked-image shell links and runtime behavior remain CI
checks, not locally observed results.

Installed QA verifies the RPM and an 86-entry manifest covering the original
85 test members plus XSL. It copies this payload into a fresh writable directory,
links the installed executable and replays both unchanged suites with explicit
Bash. Separate checks cover exact version/help streams, external printf format,
xml2csv file/stdin round trips and an input error. Generated Bash output is
never evaluated by authored QA. `LC_ALL=C` preserves byte fixtures. The complete
source archive stays in the SRPM; `make dist` would omit tests and is not used.

## Dependency and ownership boundary

Build dependencies are autoconf >= 2.69, automake, bash, coreutils, diffutils,
findutils, gcc, glibc-devel, grep, libxslt, m4, make, sed and util-linux.
Installed full-suite QA intentionally requires bash, coreutils, diffutils,
findutils, grep, libxslt, sed and util-linux. Joined official filelists identify
xsltproc in libxslt, hexdump in util-linux and all declared command providers.
The official-only static closure selects 222 riscv64/noarch production packages
and satisfies 217 versioned edges, with no missing dependency. This is provider
matching, not a target DNF/SAT transaction or ELF dependency observation.

The current official primary/filelists join covers all 18,503 packages and
2,207,942 file rows. Component names, `xml2csv`, and projected executable, man,
data, docs, license, test and debug roots have no official ownership collision.
Current managed/open-PR identity screening is separate from that provider check.
Supplemental public state was unavailable in this round and its current namespace
is not claimed verified. No supplemental package is needed for this candidate's
declared dependency closure. CI must record its actual resolution or documented
official-only fallback; publication retains its independent public-state gate.

RPM macro-expanded license/docs, compressed man aliases, build-ID/debug paths,
actual headers/payloads, ELF requirements, original-suite results and installed
smoke remain exact-product CI acceptance checks. Do not infer RPM/SRPM publication
from routing-only green checks or local repository validation.
