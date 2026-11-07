# Class::Exporter 0.03

Pure-Perl object-method exports with per-importing-package state, packaged for
openEuler 24.03 LTS SP3 riscv64/RVA23.

## Fixed source and rights

Official archive: https://cpan.metacpan.org/authors/id/S/SP/SPLICE/Class-Exporter-0.03.tar.gz
SHA-256 `362bcf3500afd488e2aec137ca07ebdce7b5469d59c5337f9e778ed356af9ef1`,
20,687 bytes, matched to fresh official metadata and PAUSE CHECKSUMS. The
historical index signature uses SHA-1 and an expired signing subkey under
official primary `2E66557AB97C19C791AF8E20328DA867450F89EC`; it is advisory,
not current strong or detached archive authentication. Mandatory archive SHA-256
is unchanged. Fedora discovery lineage is retained, not executed.

David James's existing source/README same-Perl grant remains unchanged. Original
bundled Test::Simple0.35, Test::More0.34 and Test::Builder0.06 retain their own
Schwern/chromatic notices and grants; they are not installed as runtime modules.
The source explicitly credits Exporter::Lite and Exporter::Heavy. Matched
inherited content remains in Schwern's explicitly licensed Exporter-Lite0.02
(SHA-256 `20c1e9b7ddc017b788feb34c032fc585e2c5b46a484e93f519373fd18830ce0e`),
not an inferred grant from the earlier0.01 module. The five symbol-dispatch
alternatives match the official Perl perl-5.6.1 Heavy source (Git blob
`6647f7075cbff490945e98d890911302adf62a79`) with changed variable names and
the candidate's object-bound function closure. No whole-function exact-copy
claim is made. Added DONOR-LICENSE preserves original Schwern attribution/grant,
Perl README Larry Wall1989-2001 copyright and complete Artistic/Copying terms.
Only trailing horizontal whitespace is normalized in the added copies; all nine
original archive members, including mixed line endings, remain byte-identical.
No donor source archive is included in SRPM.

## Tests and target boundaries

Original Makefile.PL and make test remain unchanged. The test explicitly uses
t/lib; host %INC confirms the bundled Test helpers are selected. Host Perl5.34.1
passes the original one-file/four-assertion default suite with zero skips before
and after the notice-only patch. PERL_TEST_ALL's optional multi-Perl author
behavior is unchanged. Installed smoke checks default value, mutation and state
independence across importing packages. Perl5.005 maps to dotted RPM5.5.

GNU patch fuzz=0, exact original hashes, actual CI patch policy, verified sources
and repository gates are retained. No recipe dependency download; network=false
does not claim physical network isolation. Host/source-only evidence is not
RISC-V RPM build/install acceptance. Exact-head target tests, installation/smoke
and physical RPM/SRPM remain required; no local RPM/QEMU build; auto-merge off.
