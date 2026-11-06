# Hash::Util::FieldHash::Compat 0.11

Official source: `https://cpan.metacpan.org/authors/id/E/ET/ETHER/Hash-Util-FieldHash-Compat-0.11.tar.gz`.
The publisher `CHECKSUMS` in the same directory records SHA-256
`642e46a75b537ba11420b30f8b03403c90a06a15458cd8009f339fe9e5f3741b`.
The archive has one safe root, only regular files/directories, and no patches.

The copyright holder's official `LICENCE` expressly grants Perl 5 dual terms,
including GPL version 1 or later and Artistic License 1.0. The RPM installs
that complete notice as its license file.

The unmodified local default `make test` passes both files and 27 assertions
without skips. The distribution also contains `xt/author` and `xt/release`
checks, which are not part of its default `t/*.t` pattern. The SPEC preserves
the default invocation and includes both distributed Perl modules.

The official SP3 RVA23 primary provides native `Hash::Util::FieldHash`, so
this fixed target uses the source's fast delegation path. Its conditional
legacy fallback requires `Tie::RefHash::Weak` only on older Perl without the
native module; the fallback source is retained, not stripped. The initial
exact-head hosted build passed all 27 assertions but DNF could not install
the RPM because RPM's static scanner inferred an unavailable
`perl(Tie::RefHash::Weak) >= 0.08` requirement from that unreachable fallback.
The first repair build also passed all 27 assertions but retained that
versioned auto-Requires: its name-only filter did not match the complete
generated dependency string. The SPEC hard-requires native
`perl(Hash::Util::FieldHash)` and now filters only the exact fallback module
name with an optional version suffix. Installed smoke checks both the native
Requires and absence of the fallback Requires. A successful target
install/smoke still requires fresh exact-head hosted CI; it is not inferred
from either prior build or the local Perl 5.34.1 run.

The frozen 151,852-row inventory records Ubuntu `0.11-2` lineage; it is not
the authority for source, license, dependencies or test results.
