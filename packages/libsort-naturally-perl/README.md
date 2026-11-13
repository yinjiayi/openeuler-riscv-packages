<!-- SPDX-License-Identifier: Apache-2.0 -->
# libsort-naturally-perl

This directory packages [Sort::Naturally 1.03](https://metacpan.org/release/BINGOS/Sort-Naturally-1.03) for openEuler 24.03 LTS SP3 on `riscv64`/RVA23 as `perl-sort-naturally`. Debian's stable package is discovery lineage; the official CPAN archive is the source.

The recipe builds the unchanged Perl module and runs both original default tests. The installed smoke test checks the version, numeric ordering inside strings, and the comparison function. No architecture patch is needed.

The module and original documentation retain Sean M. Burke's grant under the same terms as Perl. The generated `WriteMakefile1` subroutine in `Makefile.PL` matches the build-only GPL-3.0-only helper in Alexandr Ciornii's App-EUMM-Upgrade 0.21. The helper is not installed as Perl code. The combined source license accounts for both grants; the package includes the original notice, precise donor attribution and the three full pinned license texts.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
