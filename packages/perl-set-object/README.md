# Set::Object 1.43

Set::Object implements unordered collections of Perl scalars and references
using XS, including union/intersection/difference and weak references.
Upstream explicitly states that it is not thread-safe; this is not a
concurrent-container or memory-safety assurance.

## Source and lineage

Official source: `https://cpan.metacpan.org/authors/id/R/RU/RURBAN/Set-Object-1.43.tar.gz`.
SHA-256: `e3b3c7c7ecb91ef6d20eb06bf6bff74e41c40b75bd234e107d2ecf78d3dea9d1`.
Debian stable libset-object-perl 1.42-1 supplies lineage; the independently
checked current official stable release is 1.43. Exact module/RPM/path aliases
are screened against all open PRs and both target provider indexes.

The official CHECKSUMS index has a valid PAUSE-primary-bound SHA-512 signature
with the current 2027 signing subkey. Its policy is advisory; it is not a
detached archive signature. The bundled SIGNATURE has 67 exact SHA-256 member
digests and a mathematically valid historical RIPEMD160 signature. Its
keyserver certificate does not independently authenticate the author's identity.
Mandatory archive SHA-256 and official HTTPS provenance are separate evidence.

## Component licenses

Original LICENSE and Makefile.PL declare Artistic 2.0. The module independently
retains Jean-Louis Leroy, Sam Vilain, Catalyst IT, cPanel and Reini Urban grants;
Catalyst's narrower Perl Artistic grant is not overridden by distribution
metadata. Bundled ppport.h 3.13 retains Holland-Moritz, Marquess and Albanowski
notices under Perl terms; its Perl Artistic branch is used here.

The package expression is Artistic-2.0 AND Artistic-1.0-Perl for these separate
components, not a claim that their original grants were replaced. Patch0 only
adds the full ten-section Perl Artistic text and scope/copyright notices.
It changes no original file, runtime or test. This generic notice patch is not
RISC-V-specific; remove it once upstream ships equivalent full component notices.

## Tests and boundaries

The original MakeMaker test glob t/*/*.t and complete make test are retained.
Private macOS host validation passed 458 assertions across 50 selected files.
Eight original files self-skip for author-only, optional dependency or upstream
TODO conditions; no downstream skip/filter or author environment flag is added.
XS is compiled on the host, but that is not a RISC-V or installed-RPM result.
The target install recipe requires the actual Object.so; installed smoke checks
set operations and weak-reference release. Exact-head CI plus physical target
RPM/SRPM and current-main acceptance remain necessary before explicit merge.

No source download is needed by the recipe. network_during_build=false does
not assert physical CI network isolation. No source archives are committed.
