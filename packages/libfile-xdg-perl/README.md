<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-xdg-perl

The frozen inventory's exact `libfile-xdg-perl` key maps to official stable
[File-XDG 1.03](https://metacpan.org/dist/File-XDG). The CPAN `CHECKSUMS`
entry and downloaded HTTPS archive both have SHA-256
`88bd7c1458cb763beced6e7bd0c11972a156b1e39232984f8a7a8be4206bf7ce`.
Its 31 entries form one top-level tree without traversal paths, links or
special files. The bundled `LICENSE` grants Perl GPL/Artistic terms, resolving
the frozen automated `license-blocked` flag for this exact release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-XDG` nor `perl(File::XDG)`. Path::Class, Path::Tiny
and Ref::Util are available. Path::Class is declared as an explicit runtime
dependency because the default API loads it dynamically by name. This is a
snapshot check, not a guarantee about future repository state.

`%check` keeps both upstream default files. The XDG lookup tests create files
under HOME; their test process receives a fresh temporary HOME and no inherited
XDG home overrides, avoiding writes to the runner's real home. The installed
smoke verifies the Perl auto-Provide and default configuration path without
creating a real user configuration file. Exact target results await CI.

Successful PR CI artifacts alone do not prove public RPM repository publication.
