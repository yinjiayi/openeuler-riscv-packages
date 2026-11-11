<!-- SPDX-License-Identifier: Apache-2.0 -->
# libconvert-nls-date-format-perl

This package installs the architecture-independent Perl module
[`Convert::NLS_DATE_FORMAT` 0.06](https://metacpan.org/release/KOLIBRIE/Convert-NLS_DATE_FORMAT-0.06)
as `perl-convert-nls-date-format` on openEuler 24.03 LTS SP3 (riscv64/RVA23).
It converts Oracle format strings to POSIX `strftime` format strings and back.

- The CPAN archive SHA-256 matches the authorized MetaCPAN release metadata
  and the author directory's PAUSE `CHECKSUMS`. The latter has a historical
  SHA-1 OpenPGP signature by a now-expired PAUSE signing subkey; it is
  provenance evidence, not a detached signature on the archive.
- The archive includes complete GPL-1.0-or-later and Artistic-1.0-Perl terms.
  The generated `Build.PL` matches Minilla v3.0.1's ModuleBuildTiny template;
  Source1 supplies its full license at the fixed upstream commit.
  `SOURCE-DONOR-NOTICE` preserves the DateTime 0.28 and TimeDate 1.16
  (Date::Format) tokenizer attributions.
- The default offline build uses the target repository's Perl, Module::Build::Tiny
  and Test::More. `%check` runs the untouched `Build test --verbose` suite:
  `t/00_compile.t`, `t/oracle2posix.t` and `t/posix2oracle.t`. The
  installed-package smoke test exercises both conversion directions.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
