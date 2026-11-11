# sipcalc 1.1.6

The actual author homepage and download page call version1.1.6 (20130114)
latest/stable; configure.ac and the retained ChangeLog agree. Source SHA256 is
`cfd476c667f7a119e49eb5fe8adcfb9d2339bc2e0d4d01a1d64b7c229be56357`.
Observed literal HTTP author links were explicitly upgraded to the same
www.routemeister.net path over verified HTTPS. This is a transport change,
not a claim the original HTML offered HTTPS. URLs remain mutable; observed
SHA256 is not a publisher-authenticated digest. No integrity/signature link
was offered in the retained actual author/download pages; no guessed sidecar,
Git identity, historical attestation or global signature-absence claim.

All32 original release files, including Latin1 ChangeLog and generated
Autotools material, are preserved verbatim before applying the patch as
`source-notices/<relative>.notice` with32-entry SHA256SUMS. Main implementation
and accompanying files have Simon Ekstrand's full BSD-3-Clause grant.
Generated configure has FSFUL permission; aclocal/Makefile.in notices have
FSFULLR permission. install-sh retains full X11 grant and FSF modifications'
public-domain statement; mkinstalldirs explicitly says public domain. These
original statements define LicenseRef-Public-Domain, not an invented grant.
The original depcomp/missing GPL2-or-later notices and complete Autoconf
package-distribution exceptions remain unmodified; the GPL3-or-later branch
is elected and full official GPL3 text ships. Composite license describes
all source-distribution material, not a claim the CLI implementation became
GPL-only. New packaging and strict shell QA are Apache-2.0 with full text.

The package retains original configure/all/install, interface and DNS features,
manual and every option. No config.guess/sub exists or is required by this
configure; age alone is not a RISC-V blocker. Original make check is invoked;
all four generated check-am targets only depend on all-am and register zero
functional programs. Its success is not functional coverage. Nothing is
removed to manufacture a test count.

One package-local patch changes four expressions in three groups in src/sub.c: bounds are
checked before looking at a possible negative cleanline index, and -6 validates
actual optarg instead of an uninitialized local expaddr. Stdin argument storage
uses the existing128-byte input bound and reserves one NUL byte, rather than
filling an unterminated19-byte buffer with valid IPv6 input. Findings are static,
not measured target failures, CVEs or security assurance. Original bytes and
full BSD notice remain preserved; modified source is plainly identified.

Six added strict CLI cases use only literal numeric addresses without -d,
retain exact stdout/stderr/status and compare complete expected outputs:
version; IPv4 CIDR/host range; dotted/hex netmask equivalence; IPv6 compressed,
explicit -6 and host ranges; stdin blank/comment/two-address parsing; and an
invalid IPv4 splitmask rejected before address/interface/resolution handling.
The cases make multiple invocations but are six logical groups, not a claim
of exhaustive networking or protocol conformance. Numeric invocations still
retain upstream local interface discovery; they do not resolve hostnames or
send DNS requests. No live interface capability, performance or native-only
claim is inferred from source reading. Raw logs and byte digests are emitted
on success/failure, with actual same-file CLI path and unchanged-byte checks.
The installed ELF64/RISC-V executable must require libc.so.6 and have no RPATH.
Its checksum manifest is generated after RPM install-post, at the end of check.

Only target CI can prove compilation/build/install/functionality. Locally
source is data only; trusted repository497/source-only validation is distinct
from target testing and complete physical/debug-package namespace acceptance.
Current full provider/namespace/root-approved source/rights and fresh allopen
semantic identity gates remain mandatory before any PR. No shared catalog
release is invented and no current full Daily coverage is claimed.

The retained catalog opensuse/oss lineage label is mapped to schema category
opensuse-tumbleweed; original raw lineage remains unchanged in the private
N229 selection evidence. This is not a fresh distribution import.
