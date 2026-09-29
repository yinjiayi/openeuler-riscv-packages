<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-spec-native-perl

The frozen inventory's exact `libfile-spec-native-perl` key maps to official
stable [File-Spec-Native 1.004](https://metacpan.org/dist/File-Spec-Native).
The CPAN `CHECKSUMS` entry and downloaded HTTPS archive both have SHA-256
`41371dde1ee3b10142286d5e3fd67c2be3d6cdfadc297fc0666d227e8974ec3e`.
Its 41 entries form one top-level tree without traversal paths, links or
special files. The bundled `LICENSE` grants Perl GPL/Artistic terms.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-Spec-Native` nor `perl(File::Spec::Native)`;
it does provide Path::Class for the optional upstream cross-check. This is a
snapshot check, not a guarantee about future repository state.

`%check` retains all four default upstream test files. Path::Class is a
BuildRequires, preventing the cross-check from silently skipping;
`AUTHOR_TESTING=1` adds the module-load no-warnings assertion. Separate `xt/`
author/release suites are not part of upstream's default Makefile test target.
The installed smoke verifies the Perl auto-Provide and native path behavior.
Exact target results await CI.

Successful PR CI artifacts alone do not prove public RPM repository publication.
