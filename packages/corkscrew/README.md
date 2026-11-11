# Corkscrew 2.0

Official Arch extra 2.0-8 delegates `patpadgett/corkscrew` and the original
PKGBUILD explicitly uses its v2.0 archive. This recipe pins the same tag's
immutable commit ae4802b09e1c022e416f9654970794fb9d7ac8a2; all 21 original
regular source files are retained without local trimming or source evaluation.
The full original GPL version-2 COPYING, project GPL addition in ChangeLog,
and Tamas Szerb's base64 attribution remain intact. GPL-2.0-only is the
application expression supported by that full distribution notice and ChangeLog;
the boilerplate GPL example is not an application-specific or-later grant.
Separate generated/helper FSF grants, MIT/X11 notice and public-domain directory
helper remain in Source0/SRPM, not in a duplicate installed test source archive.

The original one-object default `all`, `make check` and binary `make install`
are retained. `check-am: all-am` contains no upstream test cases, so no invented
test-suite count is claimed. There is no upstream manual in this fixed source.
Obsolete config.guess/config.sub are refreshed from the declared target
automake package under their explicit distribution exception. The separate
generated-configure patch gives both compiler sanity probes an explicit
`int main(void)` signature and includes stdlib.h for existing exit calls in
both repeated ctype probes. All probes, conditions, flags and result decisions
remain intact. No autoreconf, compiler warning suppression or protocol option
removal is applied.
Default install is unstripped; normal RPM debug processing remains enabled.

Hosted run 39642298429 at 8a1cdc4415dacb950b97390845dda81c657057af
failed before make: config.log identifies configure:909 implicit-int as the
compiler sanity-probe error. The four-hunk patch is bound to the fixed source
bytes; it is a compiler-compatibility correction, not a RISC-V-specific fix.
The diagnostic config.log wrapper remains in place. Static applicability and
repository tooling checks do not establish target build or runtime success;
replacement exact-head CI and physical-product qualification remain required.

The MIT tests subpackage ships only downstream QA with its full MIT notice.
Target-only tests exercise usage exit255, absent/empty/whitespace/overlong-auth
file diagnostics, local
HTTP CONNECT request, bidirectional binary payload, Basic-auth header and HTTP
403 rejection. Every server binds only 127.0.0.1 on an ephemeral port, all
processes/server sockets have deadlines and cleanup, and no external proxy,
DNS resolution of the example destination, Internet connection or credential
is used. Metadata requests `network_during_build: false`; the QA itself uses
loopback and no external endpoints. This is not evidence of container network
isolation: actual CI build identity/network mode must be checked independently.

Static source review found `up = line` stores a block-local authentication
buffer's address for later use and the original unbounded `%s` read can overflow.
The dated package-local patch keeps the auth buffer in main scope, bounds the
read to 4095 bytes, rejects empty/read-failed and overlong tokens before connect,
and preserves original copyright notices and all CONNECT/forwarding dataflow.
This is a narrowly reviewed source correction, not broader security acceptance;
authenticated Basic-header and invalid-input target checks remain mandatory.
No upstream or authored QA is executed locally. Static AST/schema/patch checks
do not prove runtime behavior. Final provider/component/namespace gates, hosted
build/install, physical RPM/SRPM and debug co-installation remain pending.
