<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-text-quoted

This directory packages upstream `https://metacpan.org/dist/Text-Quoted` version `2.10` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The fixed CPAN archive is SHA-256 pinned and cross-checked against MetaCPAN
and PAUSE CHECKSUMS; Debian stable `libtext-quoted-perl` supplies lineage only.
No distribution recipe is used.

The original module and README retain Best Practical's same-Perl grant.
Eight bundled Module-Install files match the corresponding 1.19 donor files
after the original vendoring transform; ReadmeFromPod separately matches
the 0.30 donor. The additive notice preserves those grants, and the exact
ReadmeFromPod license is a second SHA-256-pinned source. All original files
and tests remain byte-for-byte unchanged.

The MakeMaker invocation limits the extra include path to its own source
directory to load the bundled installer. It does not assume an implicit
current directory in Perl's include list. The unchanged default
`make test` includes all seven upstream test files, including the
Encode-dependent regression; declared build dependencies supply Encode.
The staged package contains one installed module and its manual page.
Target build and installation are verified by hosted CI.

External source and patch licenses remain those of their respective
upstream projects; the repository license covers only original packaging.
