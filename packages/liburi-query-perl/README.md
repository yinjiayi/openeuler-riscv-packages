<!-- SPDX-License-Identifier: Apache-2.0 -->
# liburi-query-perl

The frozen Ubuntu `liburi-query-perl` 0.16-2 row in
`discovery-20260808T165000Z-9a89920c269462cd` maps to the official CPAN
URI-Query 0.16 release. The 16,505-byte archive SHA-256
`b4e62de79b468dcd7ee835e4dfd0035c83faf92e6c44b79bcdd9a50287fb8c18`
matches the publisher's `CHECKSUMS`. Its entries have a single root and
contain regular text files and directories, without symlinks or traversal.

The bundled LICENSE explicitly gives the distribution the Perl 5 choice of
GPL version 1 or later and Artistic License 1.0. The README and module POD
give the same Perl 5 terms; the test fixtures and build metadata carry no
conflicting notice. The RPM records
`GPL-1.0-or-later OR Artistic-1.0-Perl`.

Checksum-verified official openEuler 24.03 LTS SP3 `riscv64` RVA23 primary
metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no same-name RPM or `perl(URI::Query)` provider. It uniquely supplies
the Clone, YAML, URI::Escape, Carp, parent, MakeMaker, and Test::More
providers needed by the complete default build and runtime paths.

All 12 original `t/*.t` files remain unchanged. A fresh local default source
test passed 93 assertions in nine functional files. The three author/release
tests intentionally skip under their original upstream environment gates;
none is removed or disabled by this package. YAML is explicitly required
for the optional test branch in `t/03_hash.t`, so target CI exercises it.

Installed-RPM smoke checks the actual module provider, version, query
canonicalization, and clone behavior. Exact-head hosted target CI and
physical RPM/SRPM audit remain acceptance evidence; PR-only success is not
public repository publication.
