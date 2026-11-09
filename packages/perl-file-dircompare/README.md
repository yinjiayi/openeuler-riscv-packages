<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-file-dircompare

This noarch Perl package targets openEuler 24.03 LTS SP3 on riscv64/RVA23.
The fixed CPAN release File-DirCompare 0.7 matches SHA-256
b60e4d5dabc630fcfdcdf6f31fdcb6d277d3fd5375f02852eb4b51795a0b105b
in both MetaCPAN metadata and the author's CPAN CHECKSUMS index. Debian
and Ubuntu records establish discovery lineage only.

Gavin Carr's README and module POD explicitly grant the same terms as
Perl itself. The original README and module notice are installed.
The archive contains no bundled installer; eight relative fixture links
resolve to members in the same test directories and are not installed.

The recipe runs the unchanged upstream make test (eight files, 16
assertions observed on the host). The installed smoke test checks real
comparison callbacks for changed, equal and one-sided files. The build
requires no dependency download. Host tests are not target RPM evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
