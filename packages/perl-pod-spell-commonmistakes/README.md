<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-pod-spell-commonmistakes

This directory packages upstream `https://metacpan.org/dist/Pod-Spell-CommonMistakes` version `1.002` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The RPM name is `perl-Pod-Spell-CommonMistakes`; the two installed modules are
`Pod::Spell::CommonMistakes` and `Pod::Spell::CommonMistakes::WordList`.
The separately released `Pod::Spelling::CommonMistakes` is a distinct adaptor,
split out upstream in 1.002, and is not bundled or claimed by this package.

Source and admission evidence:

- Fixed official CPAN archive SHA-256:
  `2ba9ea76c049daf892ba2bdd85a07099a33be315876f55ed33a644d575324432`,
  reproduced from its bytes and matched to MetaCPAN and publisher `CHECKSUMS`.
- The bundled `SIGNATURE` verifies with fingerprint
  `92CC20B54833079222644B6319FAFBBEC18A831C`; all 22 signed file digests
  also match. This is a historical DSA/SHA1 manifest signature, not a detached
  archive signature. GnuPG reports undefined external key trust; it does not
  independently authenticate the signer's identity. The archive remains
  SHA-256 pinned in `sources.yaml`.
- The included `LICENSE` and both module notices use
  `GPL-1.0-or-later OR Artistic-1.0-Perl`; the wordlist retains its Debian
  Lintian attribution. No packaging recipe or code was copied from another RPM.
- Current Fedora 45 package `1.002-34.fc45` supplies discovery lineage.
  The old AUR metadata is stale and was not used for admission.
- The complete shared PR census and current official/supplemental
  primary/filelists indexes were checked for module, RPM and path conflicts.
  Official target providers include Pod::Spell 1.26, IO::Scalar 2.113,
  Module::Build::Tiny 0.047, ExtUtils::MakeMaker 7.70 and Test::More 1.302198.
  Supplemental HTTP metadata establishes consistency, not server authenticity.

`%check` invokes the original `./Build test` without editing or excluding any
of its three test files. Upstream itself treats `Test::Apocalypse` as optional
in `t/apocalypse.t`; that existing behavior is unchanged. The smoke test checks
version, spelling corrections, capitalization, combined checking and non-POD
input through the installed public API.

This is portable pure Perl: no RISC-V patch or native-kernel feature is needed.
Source-only and repository validation are not a target RPM build. Actual target
build, default tests, installation and smoke evidence must come from CI.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
