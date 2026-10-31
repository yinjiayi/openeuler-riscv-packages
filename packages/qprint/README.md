# Qprint 1.1

Official Arch extra1.1-3 delegates the Fourmilab release page. The original
HTTPS qprint-1.1.tar.gz is fixed by SHA-256
`ffa9ca1d51c871fb3b56a4bf0165418348cf080f01ff7e59cd04511b9665019c`.
The inspected official page advertises no detached signature or key; that is
a bounded observation, not a statement about every possible signing channel.

Preserve the original default `prog` target (qprint.c and getopt.c), normal
configure feature detection and original binary/manual install. CWEB source,
generated C/PDF, Windows binary (inert, not installed as a native command),
documentation, test generator and bundled fixture all remain in the unchanged
complete source archive shipped by qprint-tests. CWEB regeneration and the
maintainer's separate `all` documentation target are not upstream defaults.

Both upstream `make check` and `make wringer` run on the target build. Delete
the bundled wretch.bin before these targets so the original wretch generator
actually rebuilds it. A copy of the configured Makefile changes only literal
`/tmp/` paths to a unique private test directory; no command/assertion is
removed. Because upstream deliberately ignores cmp status, the downstream
driver also requires both exact success markers and rejects failure markers.
The first hosted build (PR2763, head d5f41b2aa1f0, run39583120909/1)
completed both upstream targets, but the driver misread make's echoed,
unexecuted failure branches as failures. Match whole trimmed output lines:
require each stdout success marker exactly once and reject all three actual
upstream failure markers on stdout or stderr. Keep every original command,
make exit-status check and additional functional assertion unchanged; the
new head still requires real target CI acceptance.
Installed/staged QA replays those complete targets against the installed
binary and unchanged bundled fixture without invoking a compiler; `-o` marks
only those pre-existing inputs as already made. This is distinct from the
build-phase generator check. Additional target-only bytewise roundtrips,
EBCDIC/paranoid/text modes, files/pipes, CLI and malformed-input checks run in
private temporary directories. No tests are disabled or locally executed.

COPYING is the upstream public-domain/unrestricted grant. Retain original
John Walker, Keith Bostic/Henry Spencer getopt, generated configure FSF grant,
Jules Verne quotation attribution and RFC1521 author/date notices. The latter
are retained source material, not a newly asserted blanket public-domain
dedication. Full original notices are also accessible in the unchanged archive.

The main binary retains the public-domain grant. The tests subpackage declares
`LicenseRef-Public-Domain AND MIT AND FSFUL`: the downstream QA helper includes
its complete MIT copyright, permission and disclaimer in its installed header;
the unchanged archived generated configure retains its FSF unlimited-copying,
distribution and modification notice (FSFUL). This accounting adds no new claim
over the retained RFC excerpt and does not alter any original source notices.

This draft is not provider/namespace admission, a target build result or an
installed RPM acceptance. Those gates require fresh current-main metadata,
all-open component deduplication, full dependency closure and real CI artifacts.
