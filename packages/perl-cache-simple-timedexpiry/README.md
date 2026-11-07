<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-cache-simple-timedexpiry

This directory packages upstream `https://metacpan.org/dist/Cache-Simple-TimedExpiry` version `0.27` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Sources and licensing

Official CPAN `Cache-Simple-TimedExpiry-0.27.tar.gz` is pinned to SHA-256
`4e78b7e4dd231b5571a48cd0ee1b63953f5e34790c9d020e1595a7c7d0abbe49`,
matching MetaCPAN and publisher CHECKSUMS. Upstream Makefile.PL explicitly
declares `license('perl')`, also recorded as `license: perl` in META.yml;
these declarations and the module's copyright are retained with `%license`.

All eight files below `inc/` byte-match the official Module-Install 0.64 archive
at `https://cpan.metacpan.org/authors/id/A/AU/AUDREYT/Module-Install-0.64.tar.gz`
(SHA-256 `756431a904e828136eba0049bd40ba932a828cd32c7070a80f9a25c174160e7d`).
Its README explicitly licenses that bundle under Perl's terms. These helpers
are used at build time, not installed into the binary RPM. No vendor code or
test is replaced; `-I.` makes the bundled installer visible on modern Perl.

The historical CHECKSUMS SHA-1 signature verifies to the official PAUSE primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`, with an expired-subkey warning.
The bundled SIGNATURE mathematically verifies under fingerprint
`AB4A62CF1A1A119A046239D6122F5DF7108E4046`; all 14 manifest file SHA-1 digests
match. Its keyserver-fetched certificate is not an independently verified
author-identity trust anchor. Both historical observations are advisory,
not a detached archive signature or a currently unexpired signature claim.
The committed archive SHA-256 remains mandatory.

Ubuntu resolute `libcache-simple-timedexpiry-perl` 0.27-4 and the frozen Fedora
catalog provide lineage; distribution recipes were not executed. Normalized
package/module aliases were checked against canonical directories, all open
PR files, and official/supplemental target package and file indexes.

## Tests and boundaries

The complete original `make test` is retained: 27 assertions in `t/01basic.t`,
including the original 8-, 5-, and 6-second waits. Fresh host execution passed
all 27; this is not target RPM evidence. Installed smoke checks storage, aliases,
empty/zero keys, inventory and explicit expiration. Target build and installed
smoke are pending CI for the exact PR head. Functional cache expiry is not a
timing-performance or native-hardware claim. No source patch is required.
