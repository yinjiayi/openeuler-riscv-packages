# Algorithm::Diff::XS 0.04

Official source: `https://cpan.metacpan.org/authors/id/A/AU/AUDREYT/Algorithm-Diff-XS-0.04.tar.gz`.
The publisher `CHECKSUMS` in the same directory records SHA-256
`cea89b47e1f70fa78f55f3c405491ce36d3effd9980f5c5491edffa31aa77153`.
The archive has one safe root, only regular files/directories, and no patches.

The official README and module POD explicitly grant redistribution under the
same terms as Perl itself for the library, including code derived from Joe
Schaefer. The RPM maps this to `GPL-1.0-or-later OR Artistic-1.0-Perl` and
installs README as the license notice. Bundled `inc/Module/Install` and
`ppport.h` are part of the checksum-verified source archive.

The unmodified local default `make test` passes both files and 1,004
assertions without skips when `Algorithm::Diff` 1.201 is provided from its
official SHA-256-verified CPAN archive (`0022da5982645d9ef0207f3eb9ef63e70e9713ed2340ed7b3850779b0d842a7d`).
The SPEC retains that default test invocation and the full XS implementation.

The archive and XS loader identify release 0.04, while the legacy `META.yml`
reports 0.01. Loading Algorithm::Diff 1.201 can also overwrite the Perl
package's in-memory `VERSION` string; the installed smoke therefore checks
the RPM identity and actual LCS behavior, not that unreliable variable.
Target build, install and smoke are not inferred from the local Perl 5.34.1
run.

The frozen 151,852-row inventory records Ubuntu `0.04-9` lineage; it is not
the authority for source, license, dependencies or test results.
