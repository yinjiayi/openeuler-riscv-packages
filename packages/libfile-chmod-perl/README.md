<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-chmod-perl

The frozen inventory's exact `libfile-chmod-perl` key maps to the latest
official [File-chmod 0.42](https://metacpan.org/dist/File-chmod). The CPAN
`CHECKSUMS` entry and downloaded HTTPS archive both have SHA-256
`6cafafff68bc84215168b55ede0d191dcb57f9a3201b51d61edb2858a2407795`.
The 33 archive entries form one top-level tree without traversal paths, links
or special files. The bundled `LICENSE` grants Perl GPL/Artistic terms,
resolving the frozen automated `unverified-upstream` decision.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-chmod` nor `perl(File::chmod)`. This is a snapshot
check, not a guarantee about future repository state.

`%check` keeps upstream's complete default `t/*.t` set of 19 files. With
`AUTHOR_TESTING` and `RELEASE_TESTING` unset, upstream itself conditionally
skips two author and nine release scripts; the remaining eight files execute
39 assertions. No script is deleted or separately disabled. Functional tests
change permissions only on `File::Temp` fixtures. The installed-RPM smoke
adds an owner executable bit to a temporary file and checks its mode. The
default suite passed locally on Perl 5.34.1, but target compatibility is not
claimed until exact-head CI.

Successful PR CI artifacts alone do not prove public RPM repository publication.
